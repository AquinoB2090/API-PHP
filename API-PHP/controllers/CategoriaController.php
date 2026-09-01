<?php

class CategoriaController extends BaseController
{
    public function index(): void
    {
        $stmt = $this->db()->query('SELECT * FROM categorias ORDER BY id');
        $this->json($stmt->fetchAll());
    }

    public function show(int $id): void
    {
        $stmt = $this->db()->prepare('SELECT * FROM categorias WHERE id = :id');
        $stmt->execute(['id' => $id]);
        $categoria = $stmt->fetch();

        if (!$categoria) {
            $this->json(['error' => 'Categoría no encontrada'], 404);
            return;
        }

        $this->json($categoria);
    }

    public function store(): void
    {
        $data = $this->readJson();
        $nombre = trim((string) ($data['nombre'] ?? ''));

        if ($nombre === '') {
            $this->json(['error' => 'El campo nombre es obligatorio'], 400);
            return;
        }

        $stmt = $this->db()->prepare('INSERT INTO categorias (nombre, descripcion) VALUES (:nombre, :descripcion)');
        $stmt->execute([
            'nombre' => $nombre,
            'descripcion' => $data['descripcion'] ?? null,
        ]);

        $this->json([
            'message' => 'Categoría creada',
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

        $stmt = $this->db()->prepare('UPDATE categorias SET nombre = :nombre, descripcion = :descripcion WHERE id = :id');
        $stmt->execute([
            'id' => $id,
            'nombre' => $nombre,
            'descripcion' => $data['descripcion'] ?? null,
        ]);

        $this->json(['message' => 'Categoría actualizada']);
    }

    public function delete(int $id): void
    {
        $stmt = $this->db()->prepare('DELETE FROM categorias WHERE id = :id');
        $stmt->execute(['id' => $id]);

        $this->json(['message' => 'Categoría eliminada']);
    }
}
