<?php

class Rol
{
    public ?int $id = null;
    public ?string $nombre = null;
    public ?string $descripcion = null;

    public function __construct(array $data = [])
    {
        $this->hydrate($data);
    }

    public function hydrate(array $data): void
    {
        if (isset($data['id'])) $this->id = (int) $data['id'];
        if (isset($data['nombre'])) $this->nombre = $data['nombre'];
        if (isset($data['descripcion'])) $this->descripcion = $data['descripcion'];
    }

    public function usuarios(): array
    {
        return [];
    }
}
