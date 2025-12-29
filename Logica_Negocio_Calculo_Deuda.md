# Lógica de Negocio: Cálculo de Deuda

Este documento describe la lógica de negocio implementada para la obtención y cálculo de deuda, detallando las estrategias específicas para el impuesto de Sellos y la estrategia genérica para otros impuestos.

## 1. Estrategia de Deuda de Sellos (`DeudaSellosStrategy`)

Esta estrategia maneja la lógica específica para el cálculo de deuda del impuesto de Sellos. Se prioriza el uso de datos en caché bajo ciertas condiciones de validez y vencimiento.

### Flujo de Determinación de Origen (Caché vs. Host)

El sistema decide si obtener los datos de la base de datos local (Caché) o consultar al servicio externo (Host) basándose en el siguiente flujo:

1.  **Verificación de Caché Habilitado:**
    *   Si el caché está deshabilitado o se fuerza el cálculo (`forzarCalculo = true`), se consulta directamente al Host.
    *   Si el caché está habilitado, se busca un registro existente en la base de datos (`ConsultaCache`) para el par `impuesto_objeto`.

2.  **Validación de Datos en Caché (si existe):**
    *   Si no existe registro en caché o los datos están vacíos, se consulta al Host.
    *   Si existe, se deserializa el objeto `DeudaObjetoDTO`.
    *   **Validación de Deuda Cero:**
        *   Si la deuda total es `0`:
            *   Se verifica la **Fecha de Vencimiento**.
            *   **Regla de Validez:** El caché es válido si:
                *   El objeto *aún no ha vencido* (Fecha Vencimiento >= Fecha Actual).
                *   O bien, el registro en caché se generó *después* de la fecha de vencimiento.
            *   Si no cumple esta regla, se considera inválido y se consulta al Host.
    *   **Validación de Deuda Positiva:**
        *   Si la deuda total es mayor a `0`:
            *   Se verifica la **Vigencia del Caché** estándar (configuración global de tiempo de vida del caché).
            *   Si no es vigente, se consulta al Host.

### Lógica de Cálculo desde Host

Cuando se determina que es necesario consultar al Host:

1.  **Consulta de Deuda:** Se invoca al servicio `gestionarDeudaService.getHostDeudaPorImpuestoObjeto`.
2.  **Enriquecimiento de Datos (Detalle de Sellos):**
    *   Se consulta un servicio adicional (`hostService.getDatosSellos`) para obtener detalles específicos (`SisndjccDTO`).
    *   **Cálculo de Fechas:**
        *   `Fecha Instrumento`: Se obtiene del servicio de sellos.
        *   `Fecha Vencimiento`: Se calcula sumando **15 días hábiles** a la fecha del instrumento.
    *   Se actualiza el objeto de deuda con el estado, fecha de instrumento y fecha de vencimiento calculada.
3.  **Persistencia:**
    *   Se marca el origen como "H" (Host).
    *   Se guarda el resultado (incluyendo la traza de ejecución) en el caché.

### Lógica de Uso de Caché

Cuando se utiliza el dato del caché:
1.  Se marca el origen como "C" (Caché).
2.  Si la traza está habilitada, se actualiza el registro en caché con la nueva traza de ejecución, sin modificar la fecha de registración original.

---

## 2. Estrategia de Deuda Genérica (`DeudaGenericaStrategy`)

Esta estrategia se aplica para impuestos que no requieren una lógica específica como la de Sellos. Es más directa y se basa principalmente en la vigencia temporal del caché.

### Flujo de Determinación de Origen

1.  **Verificación de Caché:**
    *   Si `forzarCalculo` es `false` y el caché está habilitado, se busca el registro.
2.  **Validación de Vigencia:**
    *   Si existe caché, se verifica únicamente si es **Vigente** (`gestionarDeudaService.getConsultaCacheVigente`).
    *   Si es vigente, se utiliza el dato del caché.
    *   Si no es vigente, no existe, o se fuerza el cálculo, se consulta al Host.

### Lógica de Cálculo desde Host

1.  **Consulta:** Se obtiene la deuda desde `gestionarDeudaService.getHostDeudaPorImpuestoObjeto`.
2.  **Persistencia:**
    *   Se marca el origen como "H".
    *   Se guarda el nuevo cálculo en el caché.

### Lógica de Uso de Caché

1.  Se marca el origen como "C".
2.  Al igual que en Sellos, se actualiza la traza en el registro de caché si la funcionalidad está habilitada.

---

## Resumen Comparativo

| Característica | Estrategia Sellos | Estrategia Genérica |
| :--- | :--- | :--- |
| **Validación Deuda = 0** | Lógica especial basada en Fecha de Vencimiento vs Fecha Actual/Registración. | Solo valida vigencia estándar del caché. |
| **Enriquecimiento de Datos** | Consulta servicio adicional de Sellos y calcula vencimiento (15 días hábiles). | No aplica. Usa datos directos del Host. |
| **Criterio Principal Caché** | Combinación de Vigencia + Lógica de Vencimiento del Instrumento. | Vigencia temporal estándar. |
