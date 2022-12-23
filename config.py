from screeninfo import get_monitors

mapWidth = 4000
mapHeight = 4000

screenWidth = get_monitors()[0].width
screenHeight = get_monitors()[0].height

projectileExplosionColor = (245, 245, 0)
projectileExplosionDuration = 0.25
projectileExplosionSize = 10

totalPlayerExplosions = 5
playerExplosionColors = ((245, 245, 0), (255, 0, 0), (255, 162, 0))
playerExplosionSize = (20, 40)
playerExplosionDuration = (1, 2)
playerExplosionRadius = (-25, 25)