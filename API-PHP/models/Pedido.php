<?php

class Pedido
{
    public ?int $id = null;
    public ?int $usuario_id = null;
    public ?string $fecha = null;
    public ?string $estado = null;
    public ?float $total = null;

    public function __construct(array $data = [])
    {
        $this->hydrate($data);
    }

    public function hydrate(array $data): void
    {
        if (isset($data['id'])) $this->id = (int) $data['id'];
        if (isset($data['usuario_id'])) $this->usuario_id = (int) $data['usuario_id'];
        if (isset($data['fecha'])) $this->fecha = $data['fecha'];
        if (isset($data['estado'])) $this->estado = $data['estado'];
        if (isset($data['total'])) $this->total = (float) $data['total'];
    }

    public function usuario(): ?Usuario
    {
        return null;
    }

    public function detalles(): array
    {
        return [];
    }
}
