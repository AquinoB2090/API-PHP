<?php

class ProductoController extends BaseController
{
    public function index(): void
    {
        $stmt = $this->db()->query('SELECT * FROM productos ORDER BY id');
        $this->json($stmt->fetchAll());
    }

    public function show(int $id): void
    {
        $stmt = $this->db()->prepare('SELECT * FROM productos WHERE id = :id');
        $stmt->execute(['id' => $id]);
        $producto = $stmt->fetch();

        if (!$producto) {
            $this->json(['error' => 'Producto no encontrado'], 404);
            return;
        }

        $this->json($producto);
    }

    public function store(): void
    {
        $data = $this->readJson();

        if (empty($data['categoria_id']) || empty($data['nombre']) || empty($data['precio'])) {
            $this->json(['error' => 'Faltan campos obligatorios: categoria_id, nombre y precio'], 400);
            return;
        }

        $stmt = $this->db()->prepare('INSERT INTO productos (categoria_id, nombre, descripcion, precio, stock, estado) VALUES (:categoria_id, :nombre, :descripcion, :precio, :stock, :estado) RETURNING id');
        $stmt->execute([
            'categoria_id' => (int) $data['categoria_id'],
            'nombre' => trim((string) $data['nombre']),
            'descripcion' => $data['descripcion'] ?? null,
            'precio' => (float) $data['precio'],
            'stock' => (int) ($data['stock'] ?? 0),
            'estado' => $data['estado'] ?? 'activo',
        ]);
        $id = $stmt->fetchColumn();

        $this->json([
            'message' => 'Producto creado',
            'id' => (int) $id,
        ], 201);
    }

    public function update(int $id): void
    {
        $data = $this->readJson();

        $stmt = $this->db()->prepare('UPDATE productos SET categoria_id = :categoria_id, nombre = :nombre, descripcion = :descripcion, precio = :precio, stock = :stock, estado = :estado WHERE id = :id');
        $stmt->execute([
            'id' => $id,
            'categoria_id' => (int) ($data['categoria_id'] ?? 0),
            'nombre' => trim((string) ($data['nombre'] ?? '')),
            'descripcion' => $data['descripcion'] ?? null,
            'precio' => (float) ($data['precio'] ?? 0),
            'stock' => (int) ($data['stock'] ?? 0),
            'estado' => $data['estado'] ?? 'activo',
        ]);

        $this->json(['message' => 'Producto actualizado']);
    }

    public function delete(int $id): void
    {
        $stmt = $this->db()->prepare('DELETE FROM productos WHERE id = :id');
        $stmt->execute(['id' => $id]);

        $this->json(['message' => 'Producto eliminado']);
    }
}
