import pygame

def loadTileMap(file):
    size = (64,64)
    margin = 0
    spacing = 0
    x0 = margin
    y0 = margin
    dx = size[0] + spacing
    dy = size[1] + spacing

    tiles = []
    image = pygame.transform.scale_by(pygame.image.load(file),4.0)
    rect = image.get_rect()
    print(rect.size)
    for y in range(y0,rect.height,dy+1):
        for x in range(x0,rect.width,dx+1):
            tile = pygame.Surface(size)
            tile.blit((image),(0,0),(x,y,*(size)))
            tiles.append(tile)
    print(f"loaded tileset with {len(tiles)} tiles from file : {file}")
    return tiles