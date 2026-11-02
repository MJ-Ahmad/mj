# ~/.bashrc

# Interactive shell check
case $- in
    *i*) ;;
      *) return;;
esac

# History
HISTSIZE=1000
HISTFILESIZE=2000

# Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Custom Prompt
PS1='\u@mj-ub:\w\$ '


alias mjweb='termux-open-url https://mj-ahmad.github.io/mj'
alias mc='termux-open-url content://com.coloros.filemanager/root/storage/emulated/0/Download/MyCommand.txt'
alias lc='cd /storage/emulated/0/Download'
alias mj='cd ~/mj'
alias qf='cd ~/qf'
alias dev='cd ~/dev'
alias task='cd ~/task'
alias tanzil='cd ~/tanzil'
alias nk='cd ~/mj/nijer-khata'
alias py='python3'
alias pys='python3 -m http.server 8000'
alias phps='php -S 0.0.0.0:8000'
alias pvenv='python3 -m venv venv'
alias venv='source venv/bin/activate'


alias cdev='cd ~/mj/mj/c-dev'
alias 26n02='cd ~/mj/mj/c-dev/02.11.2026'
alias qna='cd ~/mj/mj/c-dev/qna'
alias qnc='cd ~/mj/mj/c-dev/qnc'
alias qnh='cd ~/mj/mj/c-dev/qnh'
alias qnm='cd ~/mj/mj/c-dev/qnm'
alias crn='nano ~/mj/mj/c-dev/02.11.2026/README.md'
alias cnn='nano ~/mj/mj/c-dev/02.11.2026/note.txt'
alias cnqncn='nano ~/mj/mj/c-dev/02.11.2026/note.qnc.txt'
alias cnqnan='nano ~/mj/mj/c-dev/02.11.2026/note.qna.txt'
alias cnqnmn='nano ~/mj/mj/c-dev/02.11.2026/note.qnm.txt'
alias cnqnhn='nano ~/mj/mj/c-dev/02.11.2026/note.qnh.txt'
alias mjr='cd ~/mj/mj'
alias data='cd ~/mj/mj/data'
alias tqna='tree ~/mj/mj/c-dev/qna'
alias tqnc='tree ~/mj/mj/c-dev/qnc'
alias tqnh='tree ~/mj/mj/c-dev/qnh'
alias tqnm='tree ~/mj/mj/c-dev/qnm'
alias tdata='tree ~/mj/mj/data'
alias t26n02='tree ~/mj/mj/c-dev/02.11.2026'
alias lqna='ls ~/mj/mj/c-dev/qna'
alias lqnc='ls ~/mj/mj/c-dev/qnc'
alias lqnh='ls ~/mj/mj/c-dev/qnh'
alias lqnm='ls ~/mj/mj/c-dev/qnm'
alias ldata='ls ~/mj/mj/data'
alias l26n02='ls ~/mj/mj/c-dev/02.11.2026'
