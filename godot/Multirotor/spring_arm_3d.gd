extends SpringArm3D
# Script attaccato al nodo SpringArm3D

@export var mouse_sensitivity: float = 0.01
@export var min_pitch: float = -60.0
@export var max_pitch: float = 60.0
@onready var player_node: RigidBody3D = $"../Node3D/drone" # <-- Riferimento al tuo nodo personaggio

var pitch: float = 0.0
var yaw: float = 0.0

func _ready():
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	if player_node == null:
		# Assicurati di assegnare il nodo Player dall'Inspector!
		# Oppure cerca il nodo se il tuo setup è più complesso
		printerr("Player node not assigned to camera script!")
		set_process(false) # Disabilita lo script se non c'è il player

func _unhandled_input(event):
	if event is InputEventMouseMotion:
		yaw -= event.relative.x * mouse_sensitivity
		pitch += event.relative.y * mouse_sensitivity
		pitch = clamp(pitch, deg_to_rad(min_pitch), deg_to_rad(max_pitch))

		rotation.y = yaw
		rotation.x = pitch
		rotation.z = 0.0

func _physics_process(delta):
	# Aggiorna la posizione del SpringArm3D per seguire il personaggio
	if player_node != null:
		global_transform.origin = player_node.global_transform.origin

	# Gestione del mouse (già presente, solo per completezza)
	if Input.is_action_just_pressed("ui_cancel"):
		if Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
			Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
		else:
			Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
