org 0x7c00
jmp 0x0000:start

start:
    xor ax, ax
    mov ds, ax
    mov es, ax

    mov ax, 0x50 ;0x50<<1 = 0x500 (início de boot2.asm)
    mov es, ax
    xor bx, bx   ;posição = es<<1+bx

    jmp reset

reset:
    mov ah, 00h ;reseta o controlador de disco
    mov dl, 0   ;floppy disk
    int 13h

    jc reset    ;se o acesso falhar, tenta novamente

    jmp load

load:
    mov ah, 02h ;lê um setor do disco
    mov al, 1   ;quantidade de setores ocupados pelo boot2
    mov ch, 0   ;track 0
    mov cl, 2   ;sector 2
    mov dh, 0   ;head 0
    mov dl, 0   ;drive 0
    int 13h

    jc load     ;se o acesso falhar, tenta novamente

    jmp 0x500   ;pula para o setor de endereco 0x500 (start do boot2)

times 510-($-$$) db 0 ;512 bytes
dw 0xaa55             ;assinatura