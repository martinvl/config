import curses, os, subprocess

TITLE = 'Select things to configure (\'q\' to exit)'
INFO = 'Press enter to continue'

screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
screen.keypad(1)

curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE)
h = curses.color_pair(1)
n = curses.A_NORMAL

pos = 0
items = (
        {'name':'Vim', 'selected':False},
        {'name':'MacVim', 'selected':False},
        {'name':'Slate', 'selected':False},
        {'name':'Homebrew', 'selected':False}
        )

def draw_menu():
    global screen, pos, items

    screen.clear()
    curses.curs_set(1)         # reset doesn't do this right
    curses.curs_set(0)
    screen.addstr(1,2, TITLE, curses.A_BOLD)
    screen.addstr(4 + len(items),2, INFO)

    for i, item in zip(xrange(len(items)), items):
        screen.addstr(3 + i, 4, "[%s] %s" % ('*' if item['selected'] else ' ', item['name']), h if i == pos else n)

    screen.move(3 + pos, 5)

    c = screen.getch()

    if c == ord('j') or c == 258: # move down
        if pos < len(items)-1:
            pos += 1
    elif c == ord('k') or c == 259: # move up
        if pos > 0:
            pos -= 1
    elif c == ord(' '): # toggle select
        items[pos]['selected'] = not items[pos]['selected']
    elif c == ord('\n'):
        config()
        return
    elif c == ord('q'):
        return

    draw_menu()

def config():
    global screen, items

    screen.clear()
    curses.curs_set(1)         # reset doesn't do this right
    curses.curs_set(0)

    item_map = {}
    for item in items:
        item_map[item['name']] = item['selected']

    devnull = open(os.devnull, 'wb')
    pos = 0

    if item_map['Vim']:
        pos += 1

        screen.addstr(pos, 2, 'Configuring Vim...')
        screen.refresh()

        subprocess.call('curl melvon.com/config/vim.tar.gz > vim.tar.gz', shell=True, stdout=devnull, stderr=devnull)
        subprocess.call('tar xzf vim.tar.gz -C ~', shell=True, stdout=devnull, stderr=devnull)
        subprocess.call('rm -rf vim.tar.gz', shell=True, stdout=devnull, stderr=devnull)
        screen.addstr(pos, 2, 'Configuring Vim... Done')

    if item_map['MacVim']:
        pos += 1

        screen.addstr(pos, 2, 'Installing MacVim...')
        screen.refresh()

        subprocess.call('brew install wget', shell=True, stdout=devnull, stderr=devnull)
        subprocess.call('wget https://github.com/b4winckler/macvim/releases/download/snapshot-73/MacVim-snapshot-73-Mavericks.tbz', shell=True, stdout=devnull, stderr=devnull)
        subprocess.call('tar xjf MacVim-snapshot-73-Mavericks.tbz', shell=True, stdout=devnull, stderr=devnull)
        subprocess.call('mv MacVim-snapshot-73/MacVim.app /Applications/MacVim.app', shell=True, stdout=devnull, stderr=devnull)
        subprocess.call('mv MacVim-snapshot-73/mvim /usr/local/bin', shell=True, stdout=devnull, stderr=devnull)
        subprocess.call('ln -s /usr/local/bin/mvim /usr/local/bin/gvim', shell=True, stdout=devnull, stderr=devnull)
        subprocess.call('rm -r MacVim-snapshot-73 MacVim-snapshot-73-Mavericks.tbz', shell=True, stdout=devnull, stderr=devnull)

        screen.addstr(pos, 2, 'Installing MacVim... Done')

    if item_map['Slate']:
        pos += 1

        screen.addstr(pos, 2, 'Installing Slate...')
        screen.refresh()

        subprocess.call('curl http://slate.ninjamonkeysoftware.com/versions/slate-latest.tar.gz > slate.tar.gz', shell=True, stdout=devnull, stderr=devnull)
        subprocess.call('tar xzf slate.tar.gz', shell=True, stdout=devnull, stderr=devnull)
        subprocess.call('mv Slate.app /Applications/Slate.app', shell=True, stdout=devnull, stderr=devnull)
        subprocess.call('open /Applications/Slate.app', shell=True, stdout=devnull, stderr=devnull)
        subprocess.call('rm slate.tar.gz', shell=True, stdout=devnull, stderr=devnull)

        screen.addstr(pos, 2, 'Installing Slate... Done')

        pos += 1
        screen.addstr(pos, 2, 'Configuring Slate...')
        screen.refresh()

        subprocess.call('curl melvon.com/config/.slate > ~/.slate', shell=True, stdout=devnull, stderr=devnull)

        screen.addstr(pos, 2, 'Configuring Slate... Done')

    if item_map['Homebrew']:
        pos += 1

        screen.addstr(pos, 2, 'Installing Homebrew...')

        curses.def_prog_mode()
        os.system('ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
        curses.reset_prog_mode()   # reset to 'current' curses environment
        curses.curs_set(1)         # reset doesn't do this right
        curses.curs_set(0)

        screen.addstr(pos, 2, 'Installing Homebrew... Done')

    pos += 1
    screen.addstr(pos, 2, 'Press any key to finish')
    screen.getch()

draw_menu()
curses.endwin()
os.system('clear')
