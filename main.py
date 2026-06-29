from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
import uuid

app = FastAPI(title="Gestión de Conjunto Residencial API", version="1.0.0")

# CRUD generico server-side (persistencia multi-dispositivo)
try:
    from app.routers import data as _data_router
    app.include_router(_data_router.router)
except Exception as _e:
    import logging; logging.getLogger('uvicorn').warning('data router: %s', _e)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── MODELOS ────────────────────────────────────────────────────────────────

class Inmueble(BaseModel):
    id: str
    numero: str
    torre: Optional[str] = None
    tipo: str  # apartamento, casa, local
    piso: Optional[int] = None
    area_m2: float
    coeficiente: float
    estado: str  # ocupado, desocupado, en_venta
    propietario_nombre: str
    propietario_telefono: str
    propietario_email: str
    propietario_residente: bool
    parqueadero: Optional[str] = None
    deposito: Optional[str] = None

class InmuebleCreate(BaseModel):
    numero: str
    torre: Optional[str] = None
    tipo: str
    piso: Optional[int] = None
    area_m2: float
    coeficiente: float
    estado: str
    propietario_nombre: str
    propietario_telefono: str
    propietario_email: str
    propietario_residente: bool
    parqueadero: Optional[str] = None
    deposito: Optional[str] = None

class Residente(BaseModel):
    id: str
    inmueble_id: str
    nombre: str
    apellido: str
    tipo_documento: str
    numero_documento: str
    telefono: str
    email: str
    rol: str  # administrador, residente, propietario_no_residente, guardia, comite
    activo: bool
    fecha_ingreso: str
    vehiculos: List[str]
    mascotas: List[str]

class ResidenteCreate(BaseModel):
    inmueble_id: str
    nombre: str
    apellido: str
    tipo_documento: str
    numero_documento: str
    telefono: str
    email: str
    rol: str
    activo: bool
    fecha_ingreso: str
    vehiculos: List[str]
    mascotas: List[str]

class Visitante(BaseModel):
    id: str
    inmueble_id: str
    residente_id: str
    nombre: str
    apellido: str
    tipo_documento: str
    numero_documento: str
    telefono: Optional[str] = None
    motivo: str
    fecha_visita: str
    hora_entrada: Optional[str] = None
    hora_salida: Optional[str] = None
    estado: str  # pendiente, en_conjunto, finalizada, rechazada
    pre_autorizado: bool
    placa_vehiculo: Optional[str] = None
    observaciones: Optional[str] = None

class VisitanteCreate(BaseModel):
    inmueble_id: str
    residente_id: str
    nombre: str
    apellido: str
    tipo_documento: str
    numero_documento: str
    telefono: Optional[str] = None
    motivo: str
    fecha_visita: str
    hora_entrada: Optional[str] = None
    hora_salida: Optional[str] = None
    estado: str
    pre_autorizado: bool
    placa_vehiculo: Optional[str] = None
    observaciones: Optional[str] = None

class Pago(BaseModel):
    id: str
    inmueble_id: str
    residente_id: str
    concepto: str  # administracion, parqueadero, multa, extraordinaria, agua, gas
    monto: float
    fecha_vencimiento: str
    fecha_pago: Optional[str] = None
    estado: str  # pendiente, pagado, vencido, en_mora
    metodo_pago: Optional[str] = None  # efectivo, transferencia, pse, tarjeta
    referencia: Optional[str] = None
    periodo: str
    observaciones: Optional[str] = None

class PagoCreate(BaseModel):
    inmueble_id: str
    residente_id: str
    concepto: str
    monto: float
    fecha_vencimiento: str
    fecha_pago: Optional[str] = None
    estado: str
    metodo_pago: Optional[str] = None
    referencia: Optional[str] = None
    periodo: str
    observaciones: Optional[str] = None

# ─── DATOS SEED EN MEMORIA ──────────────────────────────────────────────────

inmuebles_db: List[dict] = [
    {
        "id": "inm-001",
        "numero": "101",
        "torre": "A",
        "tipo": "apartamento",
        "piso": 1,
        "area_m2": 72.5,
        "coeficiente": 0.0312,
        "estado": "ocupado",
        "propietario_nombre": "Carlos Andrés Restrepo",
        "propietario_telefono": "3101234567",
        "propietario_email": "carlos.restrepo@email.com",
        "propietario_residente": True,
        "parqueadero": "P-12",
        "deposito": "D-05"
    },
    {
        "id": "inm-002",
        "numero": "204",
        "torre": "A",
        "tipo": "apartamento",
        "piso": 2,
        "area_m2": 85.0,
        "coeficiente": 0.0365,
        "estado": "ocupado",
        "propietario_nombre": "María Fernanda Gómez",
        "propietario_telefono": "3209876543",
        "propietario_email": "mariafernanda.gomez@email.com",
        "propietario_residente": False,
        "parqueadero": "P-08",
        "deposito": None
    },
    {
        "id": "inm-003",
        "numero": "312",
        "torre": "B",
        "tipo": "apartamento",
        "piso": 3,
        "area_m2": 65.0,
        "coeficiente": 0.0280,
        "estado": "desocupado",
        "propietario_nombre": "Jorge Luis Martínez",
        "propietario_telefono": "3154567890",
        "propietario_email": "jorgeluis.martinez@email.com",
        "propietario_residente": False,
        "parqueadero": "P-21",
        "deposito": "D-11"
    },
    {
        "id": "inm-004",
        "numero": "401",
        "torre": "B",
        "tipo": "apartamento",
        "piso": 4,
        "area_m2": 92.0,
        "coeficiente": 0.0396,
        "estado": "ocupado",
        "propietario_nombre": "Luisa Alejandra Torres",
        "propietario_telefono": "3187654321",
        "propietario_email": "luisa.torres@email.com",
        "propietario_residente": True,
        "parqueadero": "P-03",
        "deposito": "D-02"
    },
    {
        "id": "inm-005",
        "numero": "L-01",
        "torre": None,
        "tipo": "local",
        "piso": 0,
        "area_m2": 45.0,
        "coeficiente": 0.0194,
        "estado": "ocupado",
        "propietario_nombre": "Inversiones Sánchez SAS",
        "propietario_telefono": "6014441122",
        "propietario_email": "inversiones.sanchez@email.com",
        "propietario_residente": False,
        "parqueadero": None,
        "deposito": None
    },
    {
        "id": "inm-006",
        "numero": "502",
        "torre": "C",
        "tipo": "apartamento",
        "piso": 5,
        "area_m2": 78.0,
        "coeficiente": 0.0336,
        "estado": "en_venta",
        "propietario_nombre": "Roberto Carlos Díaz",
        "propietario_telefono": "3223456789",
        "propietario_email": "roberto.diaz@email.com",
        "propietario_residente": False,
        "parqueadero": "P-15",
        "deposito": "D-08"
    }
]

residentes_db: List[dict] = [
    {
        "id": "res-001",
        "inmueble_id": "inm-001",
        "nombre": "Carlos Andrés",
        "apellido": "Restrepo Vargas",
        "tipo_documento": "CC",
        "numero_documento": "1020304050",
        "telefono": "3101234567",
        "email": "carlos.restrepo@email.com",
        "rol": "administrador",
        "activo": True,
        "fecha_ingreso": "2021-03-15",
        "vehiculos": ["ABC123", "XYZ789"],
        "mascotas": ["Firulais (Labrador)", "Michi (Gato persa)"]
    },
    {
        "id": "res-002",
        "inmueble_id": "inm-002",
        "nombre": "Pedro Felipe",
        "apellido": "Ramírez Ospina",
        "tipo_documento": "CC",
        "numero_documento": "98765432",
        "telefono": "3209876543",
        "email": "pedro.ramirez@email.com",
        "rol": "residente",
        "activo": True,
        "fecha_ingreso": "2022-06-01",
        "vehiculos": ["DEF456"],
        "mascotas": []
    },
    {
        "id": "res-003",
        "inmueble_id": "inm-004",
        "nombre": "Luisa Alejandra",
        "apellido": "Torres Medina",
        "tipo_documento": "CC",
        "numero_documento": "45678901",
        "telefono": "3187654321",
        "email": "luisa.torres@email.com",
        "rol": "comite",
        "activo": True,
        "fecha_ingreso": "2020-11-20",
        "vehiculos": ["GHI012"],
        "mascotas": ["Canela (Beagle)"]
    },
    {
        "id": "res-004",
        "inmueble_id": "inm-001",
        "nombre": "Andrés Felipe",
        "apellido": "Guarín López",
        "tipo_documento": "CC",
        "numero_documento": "11223344",
        "telefono": "3312345678",
        "email": "andres.guarin@conjunto.com",
        "rol": "guardia",
        "activo": True,
        "fecha_ingreso": "2023-01-10",
        "vehiculos": [],
        "mascotas": []
    },
    {
        "id": "res-005",
        "inmueble_id": "inm-002",
        "nombre": "María Fernanda",
        "apellido": "Gómez Castro",
        "tipo_documento": "CC",
        "numero_documento": "55667788",
        "telefono": "3209876543",
        "email": "mariafernanda.gomez@email.com",
        "rol": "propietario_no_residente",
        "activo": True,
        "fecha_ingreso": "2022-06-01",
        "vehiculos": [],
        "mascotas": []
    },
    {
        "id": "res-006",
        "inmueble_id": "inm-004",
        "nombre": "Santiago",
        "apellido": "Torres Medina",
        "tipo_documento": "TI",
        "numero_documento": "1000234567",
        "telefono": "3187654321",
        "email": "santiago.torres@email.com",
        "rol": "residente",
        "activo": True,
        "fecha_ingreso": "2020-11-20",
        "vehiculos": [],
        "mascotas": ["Canela (Beagle)"]
    }
]

visitantes_db: List[dict] = [
    {
        "id": "vis-001",
        "inmueble_id": "inm-001",
        "residente_id": "res-001",
        "nombre": "Juliana",
        "apellido": "Pérez Rojas",
        "tipo_documento": "CC",
        "numero_documento": "72345678",
        "telefono": "3156789012",
        "motivo": "Visita familiar",
        "fecha_visita": "2026-06-29",
        "hora_entrada": "14:30",
        "hora_salida": None,
        "estado": "en_conjunto",
        "pre_autorizado": True,
        "placa_vehiculo": "JKL345",
        "observaciones": None
    },
    {
        "id": "vis-002",
        "inmueble_id": "inm-002",
        "residente_id": "res-002",
        "nombre": "Técnico",
        "apellido": "Claro Colombia",
        "tipo_documento": "NIT",
        "numero_documento": "800123456",
        "telefono": "6016789000",
        "motivo": "Reparación internet",
        "fecha_visita": "2026-06-29",
        "hora_entrada": "10:00",
        "hora_salida": "11:30",
        "estado": "finalizada",
        "pre_autorizado": True,
        "placa_vehiculo": None,
        "observaciones": "Técnico autorizado empresa Claro"
    },
    {
        "id": "vis-003",
        "inmueble_id": "inm-004",
        "residente_id": "res-003",
        "nombre": "Ricardo",
        "apellido": "Montoya Salazar",
        "tipo_documento": "CC",
        "numero_documento": "83456789",
        "telefono": "3198765432",
        "motivo": "Reunión de negocios",
        "fecha_visita": "2026-06-30",
        "hora_entrada": None,
        "hora_salida": None,
        "estado": "pendiente",
        "pre_autorizado": True,
        "placa_vehiculo": "MNO678",
        "observaciones": None
    },
    {
        "id": "vis-004",
        "inmueble_id": "inm-001",
        "residente_id": "res-001",
        "nombre": "Delivery",
        "apellido": "Rappi Express",
        "tipo_documento": "NIT",
        "numero_documento": "900567890",
        "telefono": None,
        "motivo": "Entrega domicilio",
        "fecha_visita": "2026-06-28",
        "hora_entrada": "19:45",
        "hora_salida": "19:52",
        "estado": "finalizada",
        "pre_autorizado": False,
        "placa_vehiculo": None,
        "observaciones": "Visitante no pre-autorizado, autorizado en portería"
    },
    {
        "id": "vis-005",
        "inmueble_id": "inm-002",
        "residente_id": "res-002",
        "nombre": "Camila",
        "apellido": "Herrera Muñoz",
        "tipo_documento": "CC",
        "numero_documento": "94567890",
        "telefono": "3134567890",
        "motivo": "Visita social",
        "fecha_visita": "2026-07-01",
        "hora_entrada": None,
        "hora_salida": None,
        "estado": "pendiente",
        "pre_autorizado": True,
        "placa_vehiculo": None,
        "observaciones": None
    }
]

pagos_db: List[dict] = [
    {
        "id": "pag-001",
        "inmueble_id": "inm-001",
        "residente_id": "res-001",
        "concepto": "administracion",
        "monto": 385000.0,
        "fecha_vencimiento": "2026-06-05",
        "fecha_pago": "2026-06-03",
        "estado": "pagado",
        "metodo_pago": "transferencia",
        "referencia": "TRF-20260603-001",
        "periodo": "Junio 2026",
        "observaciones": None
    },
    {
        "id": "pag-002",
        "inmueble_id": "inm-002",
        "residente_id": "res-002",
        "concepto": "administracion",
        "monto": 452000.0,
        "fecha_vencimiento": "2026-06-05",
        "fecha_pago": None,
        "estado": "vencido",
        "metodo_pago": None,
        "referencia": None,
        "periodo": "Junio 2026",
        "observaciones": "Segundo mes en mora"
    },
    {
        "id": "pag-003",
        "inmueble_id": "inm-003",
        "residente_id": "res-005",
        "concepto": "administracion",
        "monto": 338000.0,
        "fecha_vencimiento": "2026-06-05",
        "fecha_pago": None,
        "estado": "vencido",
        "metodo_pago": None,
        "referencia": None,
        "periodo": "Junio 2026",
        "observaciones": None
    },
    {
        "id": "pag-004",
        "inmueble_id": "inm-004",
        "residente_id": "res-003",
        "concepto": "administracion",
        "monto": 492000.0,
        "fecha_vencimiento": "2026-07-05",
        "fecha_pago": None,
        "estado": "pendiente",
        "metodo_pago": None,
        "referencia": None,
        "periodo": "Julio 2026",
        "observaciones": None
    },
    {
        "id": "pag-005",
        "inmueble_id": "inm-001",
        "residente_id": "res-001",
        "concepto": "parqueadero",
        "monto": 120000.0,
        "fecha_vencimiento": "2026-06-05",
        "fecha_pago": "2026-06-03",
        "estado": "pagado",
        "metodo_pago": "pse",
        "referencia": "PSE-20260603-042",
        "periodo": "Junio 2026",
        "observaciones": None
    },
    {
        "id": "pag-006",
        "inmueble_id": "inm-002",
        "residente_id": "res-002",
        "concepto": "multa",
        "monto": 250000.0,
        "fecha_vencimiento": "2026-05-20",
        "fecha_pago": None,
        "estado": "en_mora",
        "metodo_pago": None,
        "referencia": None,
        "periodo": "Mayo 2026",
        "observaciones": "Infracción manual de convivencia - ruido nocturno"
    },
    {
        "id": "pag-007",
        "inmueble_id": "inm-004",
        "residente_id": "res-003",
        "concepto": "extraordinaria",
        "monto": 800000.0,
        "fecha_vencimiento": "2026-07-31",
        "fecha_pago": None,
        "estado": "pendiente",
        "metodo_pago": None,
        "referencia": None,
        "periodo": "Julio 2026",
        "observaciones": "Cuota extraordinaria reparación cubierta Torre C"
    },
    {
        "id": "pag-008",
        "inmueble_id": "inm-005",
        "residente_id": "res-005",
        "concepto": "administracion",
        "monto": 207000.0,
        "fecha_vencimiento": "2026-06-05",
        "fecha_pago": "2026-06-01",
        "estado": "pagado",
        "metodo_pago": "efectivo",
        "referencia": "EFT-20260601-007",
        "periodo": "Junio 2026",
        "observaciones": None
    }
]

# ─── UTILIDADES ─────────────────────────────────────────────────────────────

def generate_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"

def find_by_id(collection: List[dict], item_id: str) -> Optional[dict]:
    return next((item for item in collection if item["id"] == item_id), None)

# ─── ENDPOINTS: INMUEBLE ────────────────────────────────────────────────────

@app.get("/inmuebles", response_model=List[dict])
def get_inmuebles(estado: Optional[str] = None, tipo: Optional[str] = None, torre: Optional[str] = None):
    result = inmuebles_db.copy()
    if estado:
        result = [i for i in result if i["estado"] == estado]
    if tipo:
        result = [i for i in result if i["tipo"] == tipo]
    if torre:
        result = [i for i in result if i.get("torre") == torre]
    return result

@app.get("/inmuebles/{inmueble_id}")
def get_inmueble(inmueble_id: str):
    inmueble = find_by_id(inmuebles_db, inmueble_id)
    if not inmueble:
        raise HTTPException(status_code=404, detail="Inmueble no encontrado")
    return inmueble

@app.post("/inmuebles", status_code=201)
def create_inmueble(data: InmuebleCreate):
    existing = next((i for i in inmuebles_db if i["numero"] == data.numero and i.get("torre") == data.torre), None)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un inmueble con ese número y torre")
    new_inmueble = {"id": generate_id("inm"), **data.model_dump()}
    inmuebles_db.append(new_inmueble)
    return new_inmueble

@app.put("/inmuebles/{inmueble_id}")
def update_inmueble(inmueble_id: str, data: InmuebleCreate):
    inmueble = find_by_id(inmuebles_db, inmueble_id)
    if not inmueble:
        raise HTTPException(status_code=404, detail="Inmueble no encontrado")
    inmueble.update(data.model_dump())
    return inmueble

@app.delete("/inmuebles/{inmueble_id}")
def delete_inmueble(inmueble_id: str):
    inmueble = find_by_id(inmuebles_db, inmueble_id)
    if not inmueble:
        raise HTTPException(status_code=404, detail="Inmueble no encontrado")
    residentes_vinculados = [r for r in residentes_db if r["inmueble_id"] == inmueble_id]
    if residentes_vinculados:
        raise HTTPException(status_code=400, detail="No se puede eliminar: el inmueble tiene residentes asociados")
    inmuebles_db.remove(inmueble)
    return {"message": "Inmueble eliminado correctamente", "id": inmueble_id}

# ─── ENDPOINTS: RESIDENTE ───────────────────────────────────────────────────

@app.get("/residentes", response_model=List[dict])
def get_residentes(inmueble_id: Optional[str] = None, rol: Optional[str] = None, activo: Optional[bool] = None):
    result = residentes_db.copy()
    if inmueble_id:
        result = [r for r in result if r["inmueble_id"] == inmueble_id]
    if rol:
        result = [r for r in result if r["rol"] == rol]
    if activo is not None:
        result = [r for r in result if r["activo"] == activo]
    return result

@app.get("/residentes/{residente_id}")
def get_residente(residente_id: str):
    residente = find_by_id(residentes_db, residente_id)
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")
    return residente

@app.post("/residentes", status_code=201)
def create_residente(data: ResidenteCreate):
    inmueble = find_by_id(inmuebles_db, data.inmueble_id)
    if not inmueble:
        raise HTTPException(status_code=404, detail="Inmueble no encontrado")
    existing = next((r for r in residentes_db if r["numero_documento"] == data.numero_documento), None)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un residente con ese número de documento")
    new_residente = {"id": generate_id("res"), **data.model_dump()}
    residentes_db.append(new_residente)
    return new_residente

@app.put("/residentes/{residente_id}")
def update_residente(residente_id: str, data: ResidenteCreate):
    residente = find_by_id(residentes_db, residente_id)
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")
    if data.inmueble_id != residente["inmueble_id"]:
        inmueble = find_by_id(inmuebles_db, data.inmueble_id)
        if not inmueble:
            raise HTTPException(status_code=404, detail="Inmueble destino no encontrado")
    residente.update(data.model_dump())
    return residente

@app.delete("/residentes/{residente_id}")
def delete_residente(residente_id: str):
    residente = find_by_id(residentes_db, residente_id)
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")
    residentes_db.remove(residente)
    return {"message": "Residente eliminado correctamente", "id": residente_id}

@app.patch("/residentes/{residente_id}/toggle-activo")
def toggle_residente_activo(residente_id: str):
    residente = find_by_id(residentes_db, residente_id)
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")
    residente["activo"] = not residente["activo"]
    return residente

# ─── ENDPOINTS: VISITANTE ───────────────────────────────────────────────────

@app.get("/visitantes", response_model=List[dict])
def get_visitantes(
    inmueble_id: Optional[str] = None,
    residente_id: Optional[str] = None,
    estado: Optional[str] = None,
    fecha_visita: Optional[str] = None,
    pre_autorizado: Optional[bool] = None
):
    result = visitantes_db.copy()
    if inmueble_id:
        result = [v for v in result if v["inmueble_id"] == inmueble_id]
    if residente_id:
        result = [v for v in result if v["residente_id"] == residente_id]
    if estado:
        result = [v for v in result if v["estado"] == estado]
    if fecha_visita:
        result = [v for v in result if v["fecha_visita"] == fecha_visita]
    if pre_autorizado is not None:
        result = [v for v in result if v["pre_autorizado"] == pre_autorizado]
    return result

@app.get("/visitantes/{visitante_id}")
def get_visitante(visitante_id: str):
    visitante = find_by_id(visitantes_db, visitante_id)
    if not visitante:
        raise HTTPException(status_code=404, detail="Visitante no encontrado")
    return visitante

@app.post("/visitantes", status_code=201)
def create_visitante(data: VisitanteCreate):
    inmueble = find_by_id(inmuebles_db, data.inmueble_id)
    if not inmueble:
        raise HTTPException(status_code=404, detail="Inmueble no encontrado")
    residente = find_by_id(residentes_db, data.residente_id)
    if not residente:
        raise HTTPException(status_code=404, detail="Residente no encontrado")
    new_visitante = {"id": generate_id("vis"), **data.model_dump()}
    visitantes_db.append(new_visitante)
    return new_visitante

@app.put("/visitantes/{visitante_id}")
def update_visitante(visitante_id: str, data: VisitanteCreate):
    visitante = find_by_id(visitantes_db, visitante_id)
    if not visitante:
        raise HTTPException(status_code=404, detail="Visitante no encontrado")
    visitante.update(data.model_dump())
    return visitante

@app.delete("/visitantes/{visitante_id}")
def delete_visitante(visitante_id: str):
    visitante = find_by_id(visitantes_db, visitante_id)
    if not visitante:
        raise HTTPException(status_code=404, detail="Visitante no encontrado")
    visitantes_db.remove(visitante)
    return {"message": "Visitante eliminado correctamente", "id": visitante_id}

@app.patch("/visitantes/{visitante_id}/entrada")
def registrar_entrada(visitante_id: str):
    visitante = find_by_id(visitantes_db, visitante_id)
    if not visitante:
        raise HTTPException(status_code=404, detail="Visitante no encontrado")
    now = datetime.now()
    visitante["hora_entrada"] = now.strftime("%H:%M")
    visitante["fecha_visita"] = now.strftime("%Y-%m-%d")
    visitante["estado"] = "en_conjunto"
    return visitante

@app.patch("/visitantes/{visitante_id}/salida")
def registrar_salida(visitante_id: str):
    visitante = find_by_id(visitantes_db, visitante_id)
    if not visitante:
        raise HTTPException(status_code=404, detail="Visitante no encontrado")
    if visitante["estado"] != "en_conjunto":
        raise HTTPException(status_code=400, detail="El visitante no está registrado como en el conjunto")
    visitante["hora_salida"] = datetime.now().strftime("%H:%M")
    visitante["estado"] = "finalizada"
    return visitante

@app.patch("/visitantes/{visitante_id}/rechazar")
def rechazar_visitante(visitante_id: str):
    visitante = find_by_id(visitantes_db, visitante_id)
    if not visitante:
        raise HTTPException(status_code=404, detail="Visitante no encontrado")
    visitante["estado"] = "rechazada"
    return visitante

# ─── ENDPOINTS: PAGO ────────────────────────────────────────────────────────

@app.get("/pagos", response_model=List[dict])
def get_pagos(
    inmueble_id: Optional[str] = None,
    residente_id: Optional[str] = None,
    estado: Optional[str] = None,
    concepto: Optional[str] = None,
    periodo: Optional[str] = None
):
    result = pagos_db.copy()
    if inmueble_id:
        result = [p for p in result if p["inmueble_id"] == inmueble_id]
    if residente_id:
        result = [p for p in result if p["residente_id"] == residente_id]
    if estado:
        result = [p for p in result if p["estado"] == estado]
    if concepto:
        result = [p for p in result if p["concepto"] == concepto]
    if periodo:
        result = [p for p in result if p["periodo"] == periodo]
    return result

@app.get("/pagos/{pago_id}")
def get_pago(pago_id: str):
    pago = find_by_id(pagos_db, pago_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago

@app.post("/pagos", status_code=201)
def create_pago(data: PagoCreate):
    inmueble = find_by_id(inmuebles_db, data.inmueble_id)
    if not inmueble:
        raise HTTPException(status_code=404, detail="Inmueble no encontrado")
    new_pago = {"id": generate_id("pag"), **data.model_dump()}
    pagos_db.append(new_pago)
    return new_pago

@app.put("/pagos/{pago_id}")
def update_pago(pago_id: str, data: PagoCreate):
    pago = find_by_id(pagos_db, pago_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    pago.update(data.model_dump())
    return pago

@app.delete("/pagos/{pago_id}")
def delete_pago(pago_id: str):
    pago = find_by_id(pagos_db, pago_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    if pago["estado"] == "pagado":
        raise HTTPException(status_code=400, detail="No se puede eliminar un pago ya registrado como pagado")
    pagos_db.remove(pago)
    return {"message": "Pago eliminado correctamente", "id": pago_id}

@app.patch("/pagos/{pago_id}/registrar-pago")
def registrar_pago(pago_id: str, metodo_pago: str, referencia: Optional[str] = None):
    pago = find_by_id(pagos_db, pago_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    if pago["estado"] == "pagado":
        raise HTTPException(status_code=400, detail="Este pago ya fue registrado")
    pago["estado"] = "pagado"
    pago["fecha_pago"] = date.today().isoformat()
    pago["metodo_pago"] = metodo_pago
    pago["referencia"] = referencia
    return pago

# ─── ENDPOINTS: DASHBOARD / ESTADÍSTICAS ────────────────────────────────────

@app.get("/dashboard/stats")
def get_dashboard_stats():
    total_inmuebles = len(inmuebles_db)
    inmuebles_ocupados = sum(1 for i in inmuebles_db if i["estado"] == "ocupado")
    inmuebles_desocupados = sum(1 for i in inmuebles_db if i["estado"] == "desocupado")
    inmuebles_en_venta = sum(1 for i in inmuebles_db if i["estado"] == "en_venta")

    total_residentes = len(residentes_db)
    residentes_activos = sum(1 for r in residentes_db if r["activo"])

    visitantes_hoy = sum(1 for v in visitantes_db if v["fecha_visita"] == date.today().isoformat())
    visitantes_en_conjunto = sum(1 for v in visitantes_db if v["estado"] == "en_conjunto")
    visitantes_pendientes = sum(1 for v in visitantes_db if v["estado"] == "pendiente")

    total_pagos = len(pagos_db)
    pagos_pendientes = sum(1 for p in pagos_db if p["estado"] == "pendiente")
    pagos_vencidos = sum(1 for p in pagos_db if p["estado"] == "vencido")
    pagos_en_mora = sum(1 for p in pagos_db if p["estado"] == "en_mora")
    pagos_pagados = sum(1 for p in pagos_db if p["estado"] == "pagado")
    total_recaudado = sum(p["monto"] for p in pagos_db if p["estado"] == "pagado")
    total_por_recaudar = sum(p["monto"] for p in pagos_db if p["estado"] in ["pendiente", "vencido", "en_mora"])

    residentes_por_rol = {}
    for r in residentes_db:
        rol = r["rol"]
        residentes_por_rol[rol] = residentes_por_rol.get(rol, 0) + 1

    return {
        "inmuebles": {
            "total": total_inmuebles,
            "ocupados": inmuebles_ocupados,
            "desocupados": inmuebles_desocupados,
            "en_venta": inmuebles_en_venta,
            "tasa_ocupacion": round((inmuebles_ocupados / total_inmuebles) * 100, 1) if total_inmuebles > 0 else 0
        },
        "residentes": {
            "total": total_residentes,
            "activos": residentes_activos,
            "inactivos": total_residentes - residentes_activos,
            "por_rol": residentes_por_rol
        },
        "visitantes": {
            "hoy": visitantes_hoy,
            "en_conjunto": visitantes_en_conjunto,
            "pendientes": visitantes_pendientes,
            "total": len(visitantes_db)
        },
        "pagos": {
            "total": total_pagos,
            "pendientes": pagos_pendientes,
            "vencidos": pagos_vencidos,
            "en_mora": pagos_en_mora,
            "pagados": pagos_pagados,
            "total_recaudado": total_recaudado,
            "total_por_recaudar": total_por_recaudar
        }
    }

@app.get("/")
def root():
    return {
        "message": "API Gestión Conjunto Residencial",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": [
            "/inmuebles",
            "/residentes",
            "/visitantes",
            "/pagos",
            "/dashboard/stats"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)