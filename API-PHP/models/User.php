<?php

class User
{
    public ?int $id = null;
    public ?string $name = null;
    public ?string $email = null;

    public function __construct(array $data = [])
    {
        if (isset($data['id'])) $this->id = (int) $data['id'];
        if (isset($data['name'])) $this->name = $data['name'];
        if (isset($data['nombre'])) $this->name = $data['nombre'];
        if (isset($data['email'])) $this->email = $data['email'];
    }

    public static function all(): array
    {
        if (!function_exists('get_db_connection')) {
            return [];
        }

        $pdo = get_db_connection();
        $stmt = $pdo->query('SELECT id, nombre AS name, email FROM usuarios ORDER BY id LIMIT 100');

        return $stmt->fetchAll();
    }
}
