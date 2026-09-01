<?php

class RolController extends BaseController
{
    public function index(): void
    {
        $stmt = $this->db()->query('SELECT * FROM roles ORDER BY id');
        $this->json($stmt->fetchAll());
    }

    public function show(int $id): void
    {
        $stmt = $this->db()->prepare('SELECT * FROM roles WHERE id = :id');
        $stmt->execute(['id' => $id]);
        $rol = $stmt->fetch();

        if (!$rol) {
            $this->json(['error' => 'Rol no encontrado'], 404);
            return;
        }

        $this->json($rol);
    }

    public function store(): void
    {
        $data = $this->readJson();
        $nombre = trim((string) ($data['nombre'] ?? ''));

        if ($nombre === '') {
            $this->json(['error' => 'El campo nombre es obligatorio'], 400);
            return;
        }

        $stmt = $this->db()->prepare('INSERT INTO roles (nombre, descripcion) VALUES (:nombre, :descripcion)');
        $stmt->execute([
            'nombre' => $nombre,
            'descripcion' => $data['descripcion'] ?? null,
        ]);

        $this->json([
            'message' => 'Rol creado',
            'id' => (int) $this->db()->lastInsertId(),
        ], 201);
    }

    public function update(int $id): void
    {
        $data = $this->readJson();
        $nombre = trim((string) ($data['nombre'] ?? ''));

        if ($nombre === '') {
            $this->json(['error' => 'El campo nombre es obligatorio'], 400);
            return;
        }

        $stmt = $this->db()->prepare('UPDATE roles SET nombre = :nombre, descripcion = :descripcion WHERE id = :id');
        $stmt->execute([
            'id' => $id,
            'nombre' => $nombre,
            'descripcion' => $data['descripcion'] ?? null,
        ]);

        $this->json(['message' => 'Rol actualizado']);
    }

    public function delete(int $id): void
    {
        $stmt = $this->db()->prepare('DELETE FROM roles WHERE id = :id');
        $stmt->execute(['id' => $id]);

        $this->json(['message' => 'Rol eliminado']);
    }
}
