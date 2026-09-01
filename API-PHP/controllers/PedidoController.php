<?php

class PedidoController extends BaseController
{
    public function index(): void
    {
        $stmt = $this->db()->query('SELECT * FROM pedidos ORDER BY id');
        $this->json($stmt->fetchAll());
    }

    public function show(int $id): void
    {
        $stmt = $this->db()->prepare('SELECT * FROM pedidos WHERE id = :id');
        $stmt->execute(['id' => $id]);
        $pedido = $stmt->fetch();

        if (!$pedido) {
            $this->json(['error' => 'Pedido no encontrado'], 404);
            return;
        }

        $this->json($pedido);
    }

    public function store(): void
    {
        $data = $this->readJson();

        if (empty($data['usuario_id'])) {
            $this->json(['error' => 'El campo usuario_id es obligatorio'], 400);
            return;
        }

        $stmt = $this->db()->prepare('INSERT INTO pedidos (usuario_id, fecha, estado, total) VALUES (:usuario_id, :fecha, :estado, :total) RETURNING id');
        $stmt->execute([
            'usuario_id' => (int) $data['usuario_id'],
            'fecha' => $data['fecha'] ?? date('Y-m-d H:i:s'),
            'estado' => $data['estado'] ?? 'pendiente',
            'total' => (float) ($data['total'] ?? 0),
        ]);
        $id = $stmt->fetchColumn();

        $this->json([
            'message' => 'Pedido creado',
            'id' => (int) $id,
        ], 201);
    }

    public function update(int $id): void
    {
        $data = $this->readJson();

        $stmt = $this->db()->prepare('UPDATE pedidos SET usuario_id = :usuario_id, estado = :estado, total = :total WHERE id = :id');
        $stmt->execute([
            'id' => $id,
            'usuario_id' => (int) ($data['usuario_id'] ?? 0),
            'estado' => $data['estado'] ?? 'pendiente',
            'total' => (float) ($data['total'] ?? 0),
        ]);

        $this->json(['message' => 'Pedido actualizado']);
    }

    public function delete(int $id): void
    {
        $stmt = $this->db()->prepare('DELETE FROM pedidos WHERE id = :id');
        $stmt->execute(['id' => $id]);

        $this->json(['message' => 'Pedido eliminado']);
    }
}
