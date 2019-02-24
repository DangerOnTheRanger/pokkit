use std::fs::File;
use std::io::stdout;
use std::io::Read;

use diff_msg;

fn main() -> Result<(), std::io::Error> {
    let mut args = std::env::args();

    let mut f = File::open(args.next().unwrap())?;
    let mut s = File::open(args.next().unwrap())?;

    let mut f_msg = diff_msg::Msg::default();
    let mut s_msg = diff_msg::Msg::default();

    loop {
        f_msg.len = f.read(&mut f_msg)?;
        s_msg.len = s.read(&mut s_msg)?;

        f_msg.pos += s_msg.len();
        s_msg.pos += s_msg.len();

        match (f_msg.len(), s_msg.len()) {
            (0, 0) => break,

            (0, _) => {
                s_msg.msg = diff_msg::MsgType::Append();
                s_msg.write_msg(&mut stdout())?;
            }

            (_, 0) => {
                diff_msg::Msg {
                    pos: s_msg.pos,
                    msg: diff_msg::MsgType::Trunc(),
                    ..diff_msg::Msg::default()
                }
                .write_msg(&mut stdout())?;
                return Ok(());
            }

            (_, _) => {
                f_msg.len = f.read(&mut f_msg)?;
                s_msg.len = s.read(&mut s_msg)?;

                if f_msg.iter().ne(s_msg.iter()) {
                    s_msg.write_msg(&mut stdout())?;
                }
            }
        }
    }

    Ok(())
}
