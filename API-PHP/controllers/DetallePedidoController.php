<?php

class DetallePedidoController extends BaseController
{
    public function index(): void
    {
        $stmt = $this->db()->query('SELECT * FROM detalle_pedido ORDER BY id');
        $this->json($stmt->fetchAll());
    }

    public function show(int $id): void
    {
        $stmt = $this->db()->prepare('SELECT * FROM detalle_pedido WHERE id = :id');
        $stmt->execute(['id' => $id]);
        $detalle = $stmt->fetch();

        if (!$detalle) {
            $this->json(['error' => 'Detalle de pedido no encontrado'], 404);
            return;
        }

        $this->json($detalle);
    }

    public function store(): void
    {
        $data = $this->readJson();

        if (empty($data['pedido_id']) || empty($data['producto_id']) || empty($data['cantidad']) || empty($data['precio_unitario'])) {
            $this->json(['error' => 'Faltan campos obligatorios: pedido_id, producto_id, cantidad y precio_unitario'], 400);
            return;
        }

        $cantidad = (int) $data['cantidad'];
        $precioUnitario = (float) $data['precio_unitario'];
        $subtotal = $cantidad * $precioUnitario;

        $stmt = $this->db()->prepare('INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario, subtotal) VALUES (:pedido_id, :producto_id, :cantidad, :precio_unitario, :subtotal) RETURNING id');
        $stmt->execute([
            'pedido_id' => (int) $data['pedido_id'],
            'producto_id' => (int) $data['producto_id'],
            'cantidad' => $cantidad,
            'precio_unitario' => $precioUnitario,
            'subtotal' => $subtotal,
        ]);
        $id = $stmt->fetchColumn();

        $this->json([
            'message' => 'Detalle agregado',
            'id' => (int) $id,
        ], 201);
    }

    public function update(int $id): void
    {
        $data = $this->readJson();
        $cantidad = (int) ($data['cantidad'] ?? 1);
        $precioUnitario = (float) ($data['precio_unitario'] ?? 0);
        $subtotal = $cantidad * $precioUnitario;

        $stmt = $this->db()->prepare('UPDATE detalle_pedido SET pedido_id = :pedido_id, producto_id = :producto_id, cantidad = :cantidad, precio_unitario = :precio_unitario, subtotal = :subtotal WHERE id = :id');
        $stmt->execute([
            'id' => $id,
            'pedido_id' => (int) ($data['pedido_id'] ?? 0),
            'producto_id' => (int) ($data['producto_id'] ?? 0),
            'cantidad' => $cantidad,
            'precio_unitario' => $precioUnitario,
            'subtotal' => $subtotal,
        ]);

        $this->json(['message' => 'Detalle actualizado']);
    }

    public function delete(int $id): void
    {
        $stmt = $this->db()->prepare('DELETE FROM detalle_pedido WHERE id = :id');
        $stmt->execute(['id' => $id]);

        $this->json(['message' => 'Detalle eliminado']);
    }
}
