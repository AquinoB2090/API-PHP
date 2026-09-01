<?php

class Producto
{
    public ?int $id = null;
    public ?int $categoria_id = null;
    public ?string $nombre = null;
    public ?string $descripcion = null;
    public ?float $precio = null;
    public ?int $stock = null;
    public ?string $estado = null;

    public function __construct(array $data = [])
    {
        $this->hydrate($data);
    }

    public function hydrate(array $data): void
    {
        if (isset($data['id'])) $this->id = (int) $data['id'];
        if (isset($data['categoria_id'])) $this->categoria_id = (int) $data['categoria_id'];
        if (isset($data['nombre'])) $this->nombre = $data['nombre'];
        if (isset($data['descripcion'])) $this->descripcion = $data['descripcion'];
        if (isset($data['precio'])) $this->precio = (float) $data['precio'];
        if (isset($data['stock'])) $this->stock = (int) $data['stock'];
        if (isset($data['estado'])) $this->estado = $data['estado'];
    }

    public function categoria(): ?Categoria
    {
        return null;
    }

    public function detallesPedido(): array
    {
        return [];
    }
}
