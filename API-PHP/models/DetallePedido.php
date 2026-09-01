<?php

class DetallePedido
{
    public ?int $id = null;
    public ?int $pedido_id = null;
    public ?int $producto_id = null;
    public ?int $cantidad = null;
    public ?float $precio_unitario = null;
    public ?float $subtotal = null;

    public function __construct(array $data = [])
    {
        $this->hydrate($data);
    }

    public function hydrate(array $data): void
    {
        if (isset($data['id'])) $this->id = (int) $data['id'];
        if (isset($data['pedido_id'])) $this->pedido_id = (int) $data['pedido_id'];
        if (isset($data['producto_id'])) $this->producto_id = (int) $data['producto_id'];
        if (isset($data['cantidad'])) $this->cantidad = (int) $data['cantidad'];
        if (isset($data['precio_unitario'])) $this->precio_unitario = (float) $data['precio_unitario'];
        if (isset($data['subtotal'])) $this->subtotal = (float) $data['subtotal'];
    }

    public function pedido(): ?Pedido
    {
        return null;
    }

    public function producto(): ?Producto
    {
        return null;
    }
}
