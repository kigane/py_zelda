# py_zelda

## Display Surface & (regular)Surface
Display Surface就是pygame.display.set_mode((WIDTH,HEIGTH))返回的对象，通常命名为screen。总是可见的。  
Surface类似便利贴，创建的时候不可见，只有将其贴到Display Surface上才可见。  
产生Surface的方法
- pygame.Surface((WIDTH,HEIGTH))
- pygame.image.load(img_path).convert() //convert()将图片转换为pygame更好处理的形式。convert_alpha()会额外删除图片的alpha值。
Surface相关API
- surface.fill(color)

用screen.blit(surface, pos: tuple)将surface贴到屏幕的指定位置。先贴的先渲染，如果后贴的有重叠，则后贴的会覆盖先贴的。

## Colors
- 预定义 "red"
- RGB (r, g, b)
- RGB 16进制 "#ff00ec"

## 创建文字
1. 创建字体  `font = pygame.font.Font(font_type, font_size)` font_type可以指定一个ttf文件
2. 设置文字并创建Surface `text_surface = font.render(text, AA: bool, color)
3. 显示文字 `screen.blit(text_surface, pos: tuple)`

## Rectangles
- 放置Surfaces & 碰撞检测
- 获取Rectangle对象
    - pygame.Rectangle(left, top, width, height)
    - surface.get_rect(topleft=(left, top)) 宽高surface知道。将surface的topleft点放到(left, top)处。也可以指定midleft, center等。
- 使用Rectangle对象对surface进行更精确的控制。
- screen.blit(surface, rect)
- Collisions
    - rect1.colliderect(rect2) -> bool
    - rect1.collidepoint((x, y)) -> bool
- rect.inflate(x, y): rect.x = rect.x + x, rect.y = rect.y + y

## 获取鼠标位置
- pygame.mouse
    - .get_pos()
    - .get_pressed()
    - .get_visible()
    - .get_cursor()
    - .set_xxxx()
- event.type == pygame.MOUSEMOTION
    - event.pos

## 获取键盘输入
- pygame.key
    - .get_pressed() -> keys:list  `keys[pygame.K_SPACE] == True` 
- event.type == pygame.KEYDOWN
- event.type == pygame.KEYUP
    - event.key == pygame.K_SPACE

## pygame.draw
画矩形，圆形，线，点等等
- pygame.draw.rect(surf, color, rect: Rectangle) 填充
- pygame.draw.rect(surf, color, linewidth: int, border_radius: int) 只有线

## 时间
pygame.time.get_ticks() -> 从pygame.init()以来经过的时间(ms)

## Transform Surfaces
- pygame.transform.rotozoom(surf, angle, scale)

## 自定义event

```python
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, elapse: ms)

# ...

if event.type == obstacle_timer:
    # ... 
```

## Sprite
- pygame.sprite.Sprite
    - 子类需要给self.image,self.rect赋值，用于draw()
    - 子类可以覆盖self.update()方法，group.update()会自动调用该方法。
    - sprite.add(group) 添加到容器
    - 或在构造函数中调用`super().__init__(groups)`来自动添加到某容器
    - 一个sprite可以属于不同的Group
- pygame.sprite.Group Sprite的容器。作用类似Layer
- pygame.sprite.GroupSingle 只能有一个Sprite的容器
- Group的主要作用
    - 存储Sprite，并将其draw出来
    - 调用存储的Sprite的update方法


## Audio
- sound = pygame.mixer.Sound(filepath)
- sound.play()
- sound.play(loops = -1) 重复无数次
- sound.set_volume(val: 0~1)