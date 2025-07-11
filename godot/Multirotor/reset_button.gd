extends Button

@onready var drone: RigidBody3D = $"/root/World/Node3D/drone"

func _ready() -> void:
	pressed.connect(on_pressed)
	
func on_pressed():
	drone.do_reset()
