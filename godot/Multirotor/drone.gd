extends RigidBody3D

@onready var L = 0.195
@onready var p1 = Vector3(L,0,L)
@onready var p2 = Vector3(-L,0,L)
@onready var p3 = Vector3(-L,0,-L)
@onready var p4 = Vector3(L,0,-L)
@onready var packet: RigidBody3D = $"../../packet"
@onready var hook: Node3D = $"Hook"
@onready var packet_collision: CollisionShape3D = $"../../packet/CollisionShape3D"
@onready var drone: RigidBody3D = $"."


var f1 = Vector3(0,0,0)
var f2 = Vector3(0,0,0)
var f3 = Vector3(0,0,0)
var f4 = Vector3(0,0,0)
var attacched: bool = false

var initial_position
var initial_rotation
var initial_velocity
var initial_angular_velocity
var perform_reset : bool = false
var grabbed : bool = false 

# Called when the node enters the scene tree for the first time.
func _ready():
	initial_position = global_position
	initial_rotation = global_rotation
	initial_velocity = linear_velocity
	initial_angular_velocity = angular_velocity

func do_reset():
	perform_reset = true
	
func reset():
	position = initial_position
	rotation = initial_rotation
	linear_velocity = initial_velocity 
	angular_velocity = initial_angular_velocity
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	#var f = 2.5
	#var f1 = Vector3(0,f + 0.5,0)
	#var f2 = Vector3(0,f + 0.5,0)
	#var f3 = Vector3(0,f - 0.5,0)
	#var f4 = Vector3(0,f - 0.5,0)
	if Input.is_action_just_pressed("space"): # Utilizziamo l'azione predefinita "space"
		if !grabbed:
			grab_package(packet)
			grabbed = true
		else:
			drop_package(packet)
			grabbed = false
	if perform_reset:
		reset()
		perform_reset = false
		DDS.clear("f1")
		DDS.clear("f2")
		DDS.clear("f3")
		DDS.clear("f4")
	else:
		self.apply_local_force(f1, p1)
		self.apply_local_force(f2, p2)
		self.apply_local_force(f3, p3)
		self.apply_local_force(f4, p4)

func apply_local_force(force: Vector3, pos: Vector3):
	var pos_local = self.transform.basis * pos
	var force_local = self.transform.basis * force
	self.apply_force(force_local, pos_local)

func set_forces(_f1,_f2,_f3,_f4):
	f1 = Vector3(0,_f1,0)
	f2 = Vector3(0,_f2,0)
	f3 = Vector3(0,_f3,0)
	f4 = Vector3(0,_f4,0)

func get_pose():
	return [global_position, global_rotation]

func get_velocity():
	return [linear_velocity, angular_velocity]
	
	
func grab_package(package_body: RigidBody3D):
	

	package_body.sleeping = true # Mette il corpo in stato di riposo per la simulazione fisica

	# Impostare la modalità del RigidBody3D su STATIC
	# Questo fa sì che il pacco non venga più mosso dalla fisica, ma solo dal suo genitore.
	package_body.freeze = true
	package_body.freeze_mode = FREEZE_MODE_STATIC

	# Mantenere la posizione globale del pacco prima di cambiare genitore
	# Questo è FONDAMENTALE per evitare che il pacco "salti" all'origine del punto di aggancio.
	var old_global_transform = package_body.global_transform
#
	# Rimuovi il pacco dal suo genitore attuale
	if package_body.get_parent() != null:
		package_body.get_parent().remove_child(package_body)
#
	# Aggiungi il pacco come figlio del punto di aggancio del drone
	hook.add_child(package_body)

	# Reimposta la posizione del pacco in modo che sia ancorato correttamente al gancio
	# Calcola la nuova trasformazione locale rispetto al hook_point mantenendo la posizione globale.
	package_body.transform = hook.global_transform.affine_inverse() * old_global_transform
	
	# packet_collision.disabled = true
	packet.set_collision_mask_value(1,false)
	drone.set_collision_mask_value(2,false)
	
	print("Pacco agganciato!")

func drop_package(packet_body: RigidBody3D):
		
	# Rimuovi il pacco dal suo genitore (il hook_point del drone)
	if packet_body.get_parent() != null:
		packet_body.get_parent().remove_child(packet)

	# Riaggancia il pacco alla scena principale (o a un nodo "world" appropriato)
		get_tree().current_scene.add_child(packet_body)
	
	
	packet_body.transform =  drone.transform
	packet_body.freeze = false
	packet_body.freeze_mode = FREEZE_MODE_KINEMATIC # Riporta alla modalità normale
	packet_body.sleeping = false # Riattiva la simulazione
	packet_body.set_collision_mask_value(1,true)
	drone.set_collision_mask_value(2,true)

	print("Pacco rilasciato!")
