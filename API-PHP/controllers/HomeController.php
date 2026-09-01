<?php
// Controlador de ejemplo
class HomeController
{
	public function index()
	{
		http_response_code(200);
		echo json_encode(['message' => 'API-PHP en funcionamiento']);
	}
}
