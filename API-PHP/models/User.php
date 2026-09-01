<?php
// Modelo de ejemplo muy simple
class User
{
	public $id;
	public $name;
	public $email;

	public function __construct($data = [])
	{
		if (isset($data['id'])) $this->id = $data['id'];
		if (isset($data['name'])) $this->name = $data['name'];
		if (isset($data['email'])) $this->email = $data['email'];
	}

	// Ejemplo de método estático para obtener usuarios (usa get_db_connection si fuera necesario)
	public static function all()
	{
		if (function_exists('get_db_connection')) {
			$pdo = get_db_connection();
			$stmt = $pdo->query('SELECT id, name, email FROM users LIMIT 100');
			return $stmt->fetchAll();
		}
		return [];
	}
}
