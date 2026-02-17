#!/usr/bin/env python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    decript.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: macarval <macarval@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/16 21:45:13 by macarval          #+#    #+#              #
#    Updated: 2026/02/16 21:45:18 by macarval         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

cipher = "cdiiddwpgswtgt"

print(f"[*] Testando todas as 26 rotações para: {cipher}\n")

for i in range(26):
	decrypted = ""
	for char in cipher:
		if char.isalpha():
			shift = (ord(char) - ord('a') + i) % 26
			decrypted += chr(shift + ord('a'))
		else:
			decrypted += char
	print(f"Rotação {i:02d}: {decrypted}")
