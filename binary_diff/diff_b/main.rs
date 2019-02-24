use std::cmp::min;
use std::fs::File;
use std::io::stdout;
use std::io::BufRead;
use std::io::BufReader;

use msg;

fn main() -> Result<(), std::io::Error> {
    let mut args = std::env::args();
    args.next();

    let f = File::open(args.next().unwrap())?;
    let s = File::open(args.next().unwrap())?;
    let mut o = stdout();

    let mut f_buff = BufReader::new(f);
    let mut s_buff = BufReader::new(s);

    let mut pos = 0;

    loop {
        let f_block = f_buff.fill_buf()?;
        let s_block = s_buff.fill_buf()?;

        let mut s_msg: msg::Msg;
        let len;

        match (f_block.len(), s_block.len()) {
            (0, 0) => return Ok(()),

            (0, _) => {
                len = min(s_block.len(), msg::BUFFER_SIZE);
                s_msg = msg::Msg {
                    pos,
                    len,
                    msg: msg::MsgType::Append(),
                    ..msg::Msg::default()
                };

                s_msg.copy_from_slice(s_block.split_at(len).0);
                s_msg.write_msg(&mut o)?;
            }

            (_, 0) => {
                msg::Msg {
                    pos,
                    msg: msg::MsgType::Trunc(),
                    ..msg::Msg::default()
                }
                .write_msg(&mut o)?;
                return Ok(());
            }

            (_, _) => {
                len = min(min(f_block.len(), s_block.len()), msg::BUFFER_SIZE);
                s_msg = msg::Msg {
                    pos,
                    len,
                    msg: msg::MsgType::Replace(),
                    ..msg::Msg::default()
                };

                if f_block[..len].iter().ne(s_block[..len].iter()) {
                    s_msg.copy_from_slice(s_block.split_at(len).0);
                    s_msg.write_msg(&mut o)?;
                }

                f_buff.consume(len);
            }
        }
        s_buff.consume(len);
        pos += len;
    }
}
