use std::env::args;
use std::fs::File;
use std::io;
use std::io::Read;
use std::io::Write;

use msg;

fn main() -> Result<(), std::io::Error> {
    let mut args = args();
    let mut orig = Vec::new();
    let mut out = io::stdout();

    args.next();
    File::open(args.next().unwrap())
        .unwrap()
        .read_to_end(&mut orig)
        .unwrap();

    let mut patch = File::open(args.next().unwrap()).unwrap();

    let mut msg = msg::Msg::read_msg(&mut patch);
    let mut offset = 0;

    while msg.len != 0 {
        match msg.msg {
            msg::MsgType::Replace() => {
                out.write_all(&orig[offset..msg.pos])?;
                out.write_all(&msg)?;
                offset = msg.pos + msg.len;
            }

            msg::MsgType::Trunc() => {
                out.write_all(&orig[offset..msg.pos])?;
                return Ok(());
            }

            msg::MsgType::Append() => {
                out.write_all(&msg.buff)?;
            }
        }
        msg = msg::Msg::read_msg(&mut patch);
    }
    Ok(())
}
