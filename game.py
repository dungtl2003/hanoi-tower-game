"""
Run the game logic
"""
import sys
import pygame
from config import *
from hanoi_tower import (
    Disk,
    STATE,
    Pillar,
)

SRC = Pillar(SRC_COLUMN)
TARGET = Pillar(TARGET_COLUMN)
HELPER = Pillar(HELPER_COLUMN)


def solve(instructions, n, src, target, helper):
    """Solve the Ha Noi Tower problem"""
    if n == 1:
        instructions.append([src, target, helper])
        return

    solve(instructions, n - 1, src, helper, target)
    instructions.append([src, target, helper])
    solve(instructions, n - 1, helper, target, src)


def draw(win, pillars: list | tuple, steps=""):
    """Draw function"""
    win.fill([0, 0, 0])
    _ = [disk.draw(win) for pillar in pillars for disk in pillar]

    img = pygame.font.SysFont(FONT, FONT_SIZE).render(
        f"Total steps: {steps}", True, (255, 255, 255)
    )
    win.blit(img, (0, 0))

    pygame.display.update()


def generate_disks(n: int, pillar: Pillar):
    """Generate number of disks"""
    number = pillar.number

    for i in range(n):
        pillar.append(
            Disk(
                number,
                HEIGHT - (i + 1) * DEFAULT_DISK_HEIGHT,
                MAX_DISK_WIDTH - i * DISK_SIZE_DECREASE,
                DEFAULT_DISK_HEIGHT,
                DISK_COLORS[i % len(DISK_COLORS)],
            )
        )


def take_out_state(disk, max_height):
    """When moving a disk out of the current column"""
    if disk.rect.top > HEIGHT - max_height - 50 - disk.rect.height:
        dy = max(
            -VEL,
            HEIGHT - max_height - 50 - disk.rect.height - disk.rect.top,
        )
        disk.move(0, dy)
    else:
        disk.state = STATE.TRANSFER


def transfer_state(disk, dest):
    """When moving a disk to the destination column"""
    left = Disk.COLUMN_CENTERS[dest] - disk.rect.width // 2

    if disk.column < dest and disk.rect.x < left:
        dx = min(VEL, left - disk.rect.x)
        disk.move(dx, 0)
    elif disk.column > dest and disk.rect.x > left:
        dx = max(-VEL, left - disk.rect.x)
        disk.move(dx, 0)
    else:
        disk.state = STATE.PUT_IN


def put_in_state(disk, dest, top=None):
    """When moving a disk into the column"""
    if not top:
        if disk.rect.y < HEIGHT - disk.rect.height:
            dy = min(VEL, HEIGHT - disk.rect.height - disk.rect.y)
            disk.move(0, dy)
        else:
            disk.state = STATE.END
            disk.column = dest
    else:
        disk.move(0, VEL)
        collide = pygame.Rect.colliderect(disk.rect, top.rect)
        if collide:
            disk.rect.bottom = top.rect.top
            disk.state = STATE.END
            disk.column = dest


def process_states(disk, dest, max_height, top=None):
    """Process moving disk"""
    if disk.state == STATE.START:
        disk.state = STATE.TAKE_OUT
    elif disk.state == STATE.TAKE_OUT:
        take_out_state(disk, max_height)
    elif disk.state == STATE.TRANSFER:
        transfer_state(disk, dest)
    elif disk.state == STATE.PUT_IN:
        put_in_state(disk, dest, top)
    elif disk.state == STATE.END:
        pass

    return disk.state


def move(src, target, helper):
    """Move a disk from src column to destination column"""
    max_height = (
        (max(src.size(), target.size()) * DEFAULT_DISK_HEIGHT)
        if src.number == 2 or target.number == 2
        else max(src.size(), target.size(), helper.size()) * DEFAULT_DISK_HEIGHT
    )
    disk_src = src.top()
    disk_target = target.top() if target.size() > 0 else None

    if disk_src.state == STATE.END:
        disk_src.state = STATE.START

    if (
        process_states(
            disk_src,
            target.number,
            max_height,
            disk_target,
        )
        == STATE.END
    ):
        target.append(src.pop())

    return disk_src.state


def handle_quit():
    """Handle quit game event"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            sys.exit()


def handle_start():
    """Press key to start game"""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key in (
            pygame.K_RETURN,
            pygame.K_SPACE,
        ):
            return True

    return False


def get_pillar(pillars, number):
    """Get the pillar by the number of column"""
    for pillar in pillars:
        if pillar.number == number:
            return pillar

    return None


def main():
    """Main function"""
    instructions = []
    pillars = [SRC, TARGET, HELPER]
    solve(instructions, NUMBER_OF_DISKS, SRC.number, TARGET.number, HELPER.number)
    total_steps = 0
    entered = False

    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    generate_disks(NUMBER_OF_DISKS, SRC)

    while True:
        clock.tick(FPS)
        handle_quit()

        draw(window, pillars, str(total_steps))

        if not entered:
            entered = handle_start()
            if not entered:
                continue

        if not instructions:
            continue

        instruction = instructions[0]
        src = get_pillar(pillars, instruction[0])
        target = get_pillar(pillars, instruction[1])
        helper = get_pillar(pillars, instruction[2])
        if (
            move(
                src,
                target,
                helper,
            )
            == STATE.END
        ):
            total_steps += 1
            instructions.pop(0)


if __name__ == "__main__":
    main()
