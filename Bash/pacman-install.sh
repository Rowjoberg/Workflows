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
  curl \
  qBittorrent

#===Reload Bash===#
bash

#===Curl===#
curl -s https://ohmyposh.dev/install.sh | bash -s

#===Yay===#
sudo pacman -S --needed git base-devel && git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si

#===Binaries===#
oh-my-posh font install FiraCode

