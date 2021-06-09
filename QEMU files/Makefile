#primeiro estágio
boot1_file = boot1

#segundo estágio
boot2_file = boot2
boot2_pos = 1
boot2_size = 1

#kernel
kernel_file = kernel
kernel_pos = 2
kernel_size = 20

boot_disk = disk.img
block_size = 512
disk_size = 100

nasm_flags = -f bin
qemu_flags = -S -s -fda 

all: create_disk boot1_only boot2_only kernel_only write_boot1 write_boot2 write_kernel launch_qemu clean
# all: boot1_only boot2_only kernel_only write_boot1 write_boot2 write_kernel launch_qemu clean

create_disk:
	@dd if=/dev/zero of=$(boot_disk) bs=$(block_size) count=$(disk_size) status=noxfer

boot1_only:
	@nasm $(nasm_flags) $(boot1_file).asm -o $(boot1_file).bin

boot2_only:
	@nasm $(nasm_flags) $(boot2_file).asm -o $(boot2_file).bin

kernel_only:
	@nasm $(nasm_flags) $(kernel_file).asm -o $(kernel_file).bin

write_boot1:
	@dd if=$(boot1_file).bin of=$(boot_disk) bs=$(block_size) count=1 conv=notrunc status=noxfer

write_boot2:
	@dd if=$(boot2_file).bin of=$(boot_disk) bs=$(block_size) seek=$(boot2_pos) count=$(boot2_size) conv=notrunc status=noxfer

write_kernel:
	@dd if=$(kernel_file).bin of=$(boot_disk) bs=$(block_size) seek=$(kernel_pos) count=$(kernel_size) conv=notrunc

launch_qemu:
	clear
	@qemu-system-i386 $(qemu_flags) $(boot_disk)

clean:
	@rm -f *.bin $(boot_disk) *~
	clear
