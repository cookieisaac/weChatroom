# weChatroom

An online chatroom server that is based on Python standard libraries `asyncore` and `asynchat`

## Usage

### Start Server

```
python chatserver.py
```

Note: Use `netstat -anp | grep 5005` to verify the server is indeed up and running

### Start Client

```
telnet localhost 5005
login ike
say hello
look
who
logout
```

## Features

Command | Available in | Description
---|---|---
`login $name` | Login room | Used to log into the server
`logout` | Logout room | Used to log out of the server
`say statement` | Chat rooms | Used to say something
`look` | Chat rooms | Used to find out who is in the same room
`who` | Chat rooms | Used to find out who is logged into the server


## Bonus: [`screen` cheatsheet](https://www.youtube.com/watch?v=dFdqyccdWUE)

### Typical Use Cases

Use Case | ShortCut/Command
--- | ---
Open a screen session called `test` | `screen -S test`
Split into two regions | `S`
Region Top display window 0 named `Client1` | `c`, then `A`, type `Client1`
Region Bottom display window 1 named `Server1` | `Tab`, `c`, then `A`, type `Server1`
Split Top, use Right as `Client2` | `Tab`, `|`, `c`, then `A`, type `Client2`
Split Bottom, use Right as `Server2` | `Tab`, `|`, `c`, then `A`, type `Server2`
Close the `Server2` Window and Bottom Right Region | `Tab` to bottom right, `k`, then `X`
Keep only Top Left Region | `:focus up` and `:focus left` to Top Left Region, then `Q`
Kill `Client2` Window | `"` and select `Client2`, then `k`
Quit screen session | `\` and use `screen -ls` to verify 


*Note: `Ctrl-A` is omitted*

### Screen Session Lifecycle
Operation | ShortCut/Command
--- | ---
New/Open | `screen`
List | `screen -ls`
Reattach | `screen -r $SessionID/$SessionName`
Rename | `Ctrl`+`a`, Then Type `:sessionname $NEWNAME`
Detach/Exit | `Ctrl`+`a`, Then Press `d`
Kill | `Ctrl`+`a`, Then Press `\`(backslash)
Help | `Ctrl`+`a`, Then Press `?`

### Window Lifecycle in a Screen Session
Operation | ShortCut/Command
--- | ---
New | `Ctrl`+`a`, Then Press `c`
Rename | `Ctrl`+`a`, Then Press `A`(capital A)
Clear | `Ctrl`+`a`, Then Press `C`(capital C)
Kill | `Ctrl`+`a`, Then Press `k` or `K`(capital K)

### Window Navigation in a Screen Session
Operation | ShortCut/Command
--- | ---
Previous | `Ctrl`+`a`, Then Press `p`
Next | `Ctrl`+`a`, Then Press `n`
Previously Displayed | `Ctrl`+`a`, Then Press `Ctrl`+`a`
List | `Ctrl`+`a`, Then Press `"` (double quote)
Specific Number | `Ctrl`+`a`, Then Press `'` (single quote)
Specific Number | `Ctrl`+`a`, Then Press `0`/`1`/.../`9` (single digit)

### Region Lifecycle in a Screen Session
Operation | ShortCut/Command
--- | ---
Split | `Ctrl`+`a`, Then Press `S` (capital S)
Split Vertically | `Ctrl`+`a`, Then Press `|` (pipeline)
Resize | `Ctrl`+`a`, Then Press `Tab` or Type `:resize 25`
Kill Current | `Ctrl`+`a`, Then Press `X`(capital X) or Type `:remove`
Keep Only Current | `Ctrl`+`a`, Then Press `Q`(capital Q) or Type `:only`

## Region Navigation in a Screen Session
Operation | ShortCut/Command
--- | ---
Navigate | `Ctrl`+`a`, Then Press `Tab` or Type `:focus up/down/right/left`

Note: For easy navigation, use following key binding and resizing: Write to `~/.screenrc`, then reload with `Ctrl` + `a` and type `:source ~/.screenrc`. Note after the binding, use `K` to kill current window instead of previous `k`
```
# navigating regions
bind j focus down
bind k focus up
bind l focus right
bind h focus left


# resizing regions
bind + resize +5
bind - resize -5
bind = resize =
```

