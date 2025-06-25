export interface Link {
  id: string; // El ID del enlace
  title: string;
  url: string;
  description?: string; // Opcional
  tags?: string[];
  created_at?: string; // Opcional, si el backend lo devuelve
  user_id?: string; // Opcional, el backend ya sabe el user_id del token
}

// Interfaz para la creación (sin ID)
export interface LinkCreate {
  title: string;
  url: string;
  description?: string;
  tags?: string[];
}

// Interfaz para la actualización (sin ID, y todos los campos opcionales)
export interface LinkUpdate {
  title?: string;
  url?: string;
  description?: string;
  tags?: string[];
}