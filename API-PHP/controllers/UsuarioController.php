<?php

class UsuarioController extends BaseController
{
    public function index(): void
    {
        $stmt = $this->db()->query('SELECT * FROM usuarios ORDER BY id');
        $this->json($stmt->fetchAll());
    }

    public function show(int $id): void
    {
        $stmt = $this->db()->prepare('SELECT * FROM usuarios WHERE id = :id');
        $stmt->execute(['id' => $id]);
        $usuario = $stmt->fetch();

        if (!$usuario) {
            $this->json(['error' => 'Usuario no encontrado'], 404);
            return;
        }

        $this->json($usuario);
    }

    public function store(): void
    {
        $data = $this->readJson();

        if (empty($data['nombre']) || empty($data['email']) || empty($data['password']) || empty($data['rol_id'])) {
            $this->json(['error' => 'Faltan campos obligatorios: nombre, email, password y rol_id'], 400);
            return;
        }

        $stmt = $this->db()->prepare('INSERT INTO usuarios (rol_id, nombre, email, password) VALUES (:rol_id, :nombre, :email, :password) RETURNING id');
        $stmt->execute([
            'rol_id' => (int) $data['rol_id'],
            'nombre' => trim((string) $data['nombre']),
            'email' => trim((string) $data['email']),
            'password' => password_hash((string) $data['password'], PASSWORD_BCRYPT),
        ]);
        $id = $stmt->fetchColumn();

        $this->json([
            'message' => 'Usuario creado',
            'id' => (int) $id,
        ], 201);
    }

    public function update(int $id): void
    {
        $data = $this->readJson();

        $stmt = $this->db()->prepare('UPDATE usuarios SET rol_id = :rol_id, nombre = :nombre, email = :email WHERE id = :id');
        $stmt->execute([
            'id' => $id,
            'rol_id' => (int) ($data['rol_id'] ?? 0),
            'nombre' => trim((string) ($data['nombre'] ?? '')),
            'email' => trim((string) ($data['email'] ?? '')),
        ]);

        $this->json(['message' => 'Usuario actualizado']);
    }

    public function delete(int $id): void
    {
        $stmt = $this->db()->prepare('DELETE FROM usuarios WHERE id = :id');
        $stmt->execute(['id' => $id]);

        $this->json(['message' => 'Usuario eliminado']);
    }
}
