#
# ~/.bashrc
#
# eval "$(starship init bash)"
# If not running interactively, don't do anything
[[ $- != *i* ]] && return
# Set up fzf key bindings and fuzzy completion
eval "$(fzf --bash)"
alias lg=lazygit
alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '
bind 'TAB:menu-complete'
bind 'set show-all-if-ambiguous on'

#===Yazi===#
export EDITOR=nvim

function y() {
	local tmp="$(mktemp -t "yazi-cwd.XXXXXX")" cwd
	yazi "$@" --cwd-file="$tmp"
	IFS= read -r -d '' cwd < "$tmp"
	[ -n "$cwd" ] && [ "$cwd" != "$PWD" ] && builtin cd -- "$cwd"
	rm -f -- "$tmp"
}
#===Oh My Posh===#
export PATH=$PATH:/home/rowan/.local/bin
eval "$(oh-my-posh init bash)"
