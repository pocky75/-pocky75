vscode에 있는 컴파일러를 통하여 AI챗봇과 간단한 대화할 수 있는 프로그램

![스크린샷 2025-03-19 174322](https://github.com/user-attachments/assets/9bce1d50-6c96-4256-b991-8db6591c2b88)

## vscode 벽돌깨기게임 프로그램
import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("벽돌깨기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 패들 설정 (길이 증가)
PADDLE_WIDTH = 150  # 기존 100에서 150으로 증가
PADDLE_HEIGHT = 10
paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)

# 패들 이동 속도
paddle_speed = 6

# 패들 속도 증가 여부 추적
paddle_speed_increased = False

# 공 설정
BALL_RADIUS = 8
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [random.choice([-4, 4]), -4]
balls = [(ball, ball_speed, 0)]  # 공, 속도, 속도 증가 횟수

# 공 충돌 횟수 추적
collision_count = 0

# 벽돌 설정
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = SCREEN_WIDTH // BRICK_COLS - 2  # 벽돌 간 간격 추가
BRICK_HEIGHT = 20
BRICK_SPACING = 2  # 벽돌 간 간격
bricks = [pygame.Rect(col * (BRICK_WIDTH + BRICK_SPACING), row * (BRICK_HEIGHT + BRICK_SPACING), BRICK_WIDTH, BRICK_HEIGHT) for row in range(BRICK_ROWS) for col in range(BRICK_COLS)]

# 점수 초기화
score = 0

# 벽돌 추가 및 내리기 함수
def drop_and_add_bricks():
    # 기존 벽돌을 1줄 아래로 이동
    for brick in bricks:
        brick.move_ip(0, BRICK_HEIGHT + BRICK_SPACING)

    # 새로운 벽돌 1줄 추가
    for col in range(BRICK_COLS):
        new_brick = pygame.Rect(col * (BRICK_WIDTH + BRICK_SPACING), 0, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(new_brick)

# 시간 관련 설정
brick_drop_interval = 7000  # 7초 (밀리초)
last_brick_drop_time = pygame.time.get_ticks()  # 마지막 벽돌이 내려온 시간
font = pygame.font.SysFont(None, 36)  # 타이머 표시를 위한 폰트

# 게임 루프
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    # 현재 시간 계산
    current_time = pygame.time.get_ticks()
    time_until_next_drop = max(0, (brick_drop_interval - (current_time - last_brick_drop_time)) // 1000)

    # 벽돌 7초마다 1줄 내리기
    if current_time - last_brick_drop_time >= brick_drop_interval:
        drop_and_add_bricks()
        last_brick_drop_time = current_time

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 패들 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-paddle_speed, 0)
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.move_ip(paddle_speed, 0)

    # 공 이동 및 충돌 처리
    for ball, ball_speed, speed_increase_count in balls[:]:
        ball.move_ip(ball_speed)

        # 공 벽 충돌
        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]
        if ball.bottom >= SCREEN_HEIGHT:
            print("게임 오버!")
            balls.remove((ball, ball_speed, speed_increase_count))
            if not balls:  # 모든 공이 사라지면 게임 종료
                running = False

        # 공 패들 충돌
        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]
            collision_count += 1  # 충돌 횟수 증가

            # 공 추가
            if collision_count % 2 == 0:  # 두 번 충돌할 때마다 공 추가
                new_ball = pygame.Rect(ball.left, ball.top, BALL_RADIUS * 2, BALL_RADIUS * 2)
                new_ball_speed = [random.choice([-4, 4]), -4]  # 공 속도는 처음 속도로 유지
                balls.append((new_ball, new_ball_speed, 0))

        # 공 벽돌 충돌
        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_speed[1] = -ball_speed[1]
                score += 5  # 점수 5점 추가

                # 추가 충돌 시뮬레이션
                for _ in range(3):  # 3번 추가 충돌
                    for extra_brick in bricks[:]:
                        if ball.colliderect(extra_brick):
                            bricks.remove(extra_brick)
                            break
                break

    # 승리 조건
    if not bricks:
        print("승리!")
        running = False

    # 그리기
    for ball, _, _ in balls:
        pygame.draw.ellipse(screen, RED, ball)
    pygame.draw.rect(screen, WHITE, paddle)
    for brick in bricks:
        pygame.draw.rect(screen, BLUE, brick)

    # 점수 및 다음 벽돌 내려오는 시간 표시
    score_text = font.render(f"Score: {score}", True, WHITE)
    timer_text = font.render(f"Next Drop: {time_until_next_drop}s", True, WHITE)
    screen.blit(score_text, (10, 10))  # 점수는 왼쪽 상단에 표시
    screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))  # 타이머는 오른쪽 상단에 표시

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
