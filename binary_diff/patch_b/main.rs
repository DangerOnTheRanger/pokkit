use std::env::args;
use std::fs::File;
use std::io::stdout;
use std::io::Read;
use std::io::Write;

use diff_msg;

fn main() -> Result<(), std::io::Error> {
    let mut args = args();
    let mut orig = Vec::new();

    args.next();
    File::open(args.next().unwrap())
        .unwrap()
        .read_to_end(&mut orig)
        .unwrap();

    let mut patch = File::open(args.next().unwrap())?;

    let mut msg = diff_msg::Msg::read_msg(&mut patch)?;
    while msg.len != 0 {
        match msg.msg {
            diff_msg::MsgType::Replace() => unsafe {
                msg.buff
                    .as_mut_ptr()
                    .copy_to_nonoverlapping(orig.as_mut_ptr().add(msg.pos), diff_msg::BUFFER_SIZE);
            },

            diff_msg::MsgType::Trunc() => {
                orig.truncate(msg.pos + 1);
            }

            diff_msg::MsgType::Append() => {
                orig.extend_from_slice(&msg.buff);
            }
        }
        msg = diff_msg::Msg::read_msg(&mut patch)?;
    }

    stdout().write_all(&orig)?;

    Ok(())
}
