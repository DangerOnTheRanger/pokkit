pub const BUFFER_SIZE: usize = 512;

#[derive(Copy, Clone)]
pub enum MsgType {
    Replace(),
    Trunc(),
    Append(),
}

pub struct Msg {
    pub pos: usize,
    pub len: usize,
    pub buff: [u8; BUFFER_SIZE],
    pub msg: MsgType,
}

impl Msg {
    pub fn read_msg(inp: &mut impl std::io::Read) -> Result<Self, std::io::Error> {
        unsafe {
            let mut read: Self = std::mem::uninitialized();

            inp.read_exact(to_byte_slice_mut(&mut read.pos))?;
            inp.read_exact(to_byte_slice_mut(&mut read.len))?;
            inp.read_exact(&mut read.buff)?;
            inp.read_exact(to_byte_slice_mut(&mut read.msg))?;

            read.pos = usize::from_le(read.pos);
            read.len = usize::from_le(read.len);

            Ok(read)
        }
    }

    pub fn write_msg(&self, out: &mut impl std::io::Write) -> Result<(), std::io::Error> {
        unsafe {
            out.write_all(to_byte_slice(&self.pos.to_le()))?;
            out.write_all(to_byte_slice(&self.len.to_le()))?;
            out.write_all(&self.buff)?;
            out.write_all(to_byte_slice(&self.msg))?;
        }
        Ok(())
    }
}

unsafe fn to_byte_slice<T>(item: &T) -> &[u8] {
    std::slice::from_raw_parts(item as *const T as *const u8, std::mem::size_of::<T>())
}

unsafe fn to_byte_slice_mut<T>(item: &mut T) -> &mut [u8] {
    std::slice::from_raw_parts_mut(item as *mut T as *mut u8, std::mem::size_of::<T>())
}

impl std::ops::Deref for Msg {
    type Target = [u8];

    fn deref(&self) -> &[u8] {
        self.buff.split_at(self.len).0
    }
}

impl std::ops::DerefMut for Msg {
    fn deref_mut(&mut self) -> &mut [u8] {
        self.buff.split_at_mut(self.len).0
    }
}

impl Default for Msg {
    fn default() -> Self {
        Self {
            pos: 0,
            len: 0,
            buff: [0; BUFFER_SIZE],
            msg: MsgType::Replace(),
        }
    }
}
