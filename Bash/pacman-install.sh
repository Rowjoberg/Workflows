#===Arch===#
sudo pacman -S --needed \
  docker \
  nvim \
  lazydocker \
  lazygit \
  tailscale \
  ssh \
  ufw \
  yazi \
  zoxide \
  fzf \
  fd \
  curl

#===Curl===#
curl -s https://ohmyposh.dev/install.sh | bash -s

#===Reload Bash===#
bash

#===Binaries===#
oh-my-posh font install FiraCode

