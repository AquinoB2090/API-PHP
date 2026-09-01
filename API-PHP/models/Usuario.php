<?php

class Usuario
{
    public ?int $id = null;
    public ?int $rol_id = null;
    public ?string $nombre = null;
    public ?string $email = null;
    public ?string $password = null;
    public ?string $created_at = null;

    public function __construct(array $data = [])
    {
        $this->hydrate($data);
    }

    public function hydrate(array $data): void
    {
        if (isset($data['id'])) $this->id = (int) $data['id'];
        if (isset($data['rol_id'])) $this->rol_id = (int) $data['rol_id'];
        if (isset($data['nombre'])) $this->nombre = $data['nombre'];
        if (isset($data['email'])) $this->email = $data['email'];
        if (isset($data['password'])) $this->password = $data['password'];
        if (isset($data['created_at'])) $this->created_at = $data['created_at'];
    }

    public function rol(): ?Rol
    {
        return null;
    }

    public function pedidos(): array
    {
        return [];
    }
}
