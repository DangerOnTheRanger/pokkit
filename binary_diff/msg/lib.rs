pub const BUFFER_SIZE: usize = 127;

#[derive(Copy, Clone)]
pub enum MsgType {
    Replace(),
    Trunc(),
    Append(),
}

#[derive(Clone)]
pub struct Msg {
    pub pos: usize,
    pub len: usize,
    pub buff: [u8; BUFFER_SIZE],
    pub msg: MsgType,
}

impl Msg {
    pub fn from_slice(slc: &[u8], pos: usize, msg: MsgType) -> Self {
        let mut ret = Self {
            pos,
            msg,
            len: slc.len(),
            ..Self::default()
        };
        ret.copy_from_slice(slc);
        ret
    }

    pub fn read_msg(inp: &mut impl std::io::Read) -> Self {
        let mut read: Self;
        unsafe {
            read = std::mem::uninitialized();
            let sz = inp.read(to_byte_slice_mut(&mut read)).unwrap();
            if sz < std::mem::size_of::<Self>() {
                return Self::default();
            }
        }

        read.pos = usize::from_le(read.pos);
        read.len = usize::from_le(read.len);
        read
    }

    pub fn write_msg(&self, out: &mut impl std::io::Write) -> Result<(), std::io::Error> {
        let mut to_write = self.clone();
        to_write.len = to_write.len.to_le();
        to_write.pos = to_write.pos.to_le();
        unsafe {
            out.write_all(to_byte_slice(&to_write))?;
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
