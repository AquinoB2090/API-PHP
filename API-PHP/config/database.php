<?php

function sqlite_database_path(): string
{
    $configuredPath = getenv('SQLITE_PATH');

    if (is_string($configuredPath) && trim($configuredPath) !== '') {
        return $configuredPath;
    }

    if (is_dir('/home/site/data')) {
        return '/home/site/data/database.sqlite';
    }

    return __DIR__ . '/../data/database.sqlite';
}

function get_db_connection(): PDO
{
    static $pdo = null;

    if ($pdo instanceof PDO) {
        return $pdo;
    }

    $databasePath = sqlite_database_path();
    $databaseDir = dirname($databasePath);

    if (!is_dir($databaseDir)) {
        mkdir($databaseDir, 0775, true);
    }

    $pdo = new PDO(
        'sqlite:' . $databasePath,
        null,
        null,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]
    );

    $pdo->exec('PRAGMA foreign_keys = ON');
    initialize_database($pdo);

    return $pdo;
}

function initialize_database(PDO $pdo): void
{
    $migration = __DIR__ . '/../migrations/001_create_schema.sql';

    if (!is_file($migration)) {
        throw new RuntimeException('No se encontro la migracion inicial de SQLite.');
    }

    $pdo->exec(file_get_contents($migration));
}
