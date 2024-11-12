from bullet import Bullet
import collision

class EnemyBullet(Bullet):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.shape.collision_type = collision.Layer.ENEMYBULLET.value

    def update(self):
        self.ttl -= 1
        if self.ttl < 0:
            self.scene.remove_object(self)

        self.position += self.direction_vector
        self.body.position = self.position.x, self.position.y

        collisions = self.get_collisions()

        for collision_data in collisions:
            # Add more things to ignore collision with
            if collision_data["shape"].collision_type == collision.Layer.COIN.value:
                continue
            if collision_data["shape"].collision_type == collision.Layer.ENEMY.value:
                self.scene.find_rigid_body(collision_data["shape"]).deal_damage(1)
            self.scene.remove_object(self)