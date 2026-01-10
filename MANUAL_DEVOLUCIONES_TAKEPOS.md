# Manual de Devoluciones en TakePOS

## ¿Qué es una devolución?

Una devolución (también llamada abono o nota de crédito) es un documento que permite devolver dinero al cliente cuando regresa productos comprados.

## Tipos de devolución

### Devolución Total
Cuando el cliente devuelve **todos** los productos del ticket.

### Devolución Parcial
Cuando el cliente devuelve **solo algunos** productos del ticket (por ejemplo, compró 3 productos pero solo devuelve 2).

---

## ¿Cómo hacer una devolución?

### Paso 1: Buscar el ticket original

1. En TakePOS, ve al historial de tickets
2. Busca y abre el ticket que el cliente quiere devolver
3. Haz clic en el botón **"Crear Abono"**

### Paso 2: Seleccionar productos a devolver

Después de hacer clic en "Crear Abono", el sistema crea un **borrador** del abono con todos los productos.

**Para devolución parcial:**
- Elimina los productos que el cliente NO está devolviendo
- Usa el icono de la papelera (🗑️) al lado de cada producto
- Deja solo los productos que sí se van a devolver

**Para devolución total:**
- Deja todos los productos como están

### Paso 3: Validar el abono

1. Una vez que tengas los productos correctos en el abono, haz clic en el botón **"Validar"**
2. El sistema:
   - Registra el abono
   - Devuelve el stock al almacén automáticamente
   - Te muestra opciones para devolver el dinero

### Paso 4: Seleccionar método de devolución

Aparecerá un menú con 3 opciones para devolver el dinero al cliente:

- **Efectivo**: Si devuelves dinero en efectivo
- **Cheque**: Si devuelves con un cheque
- **Tarjeta**: Si devuelves a la tarjeta del cliente

Selecciona el método que vas a usar y listo.

---

## Resumen del proceso

```
1. Buscar ticket original
2. Clic en "Crear Abono"
3. Eliminar productos que NO se devuelven (si es devolución parcial)
4. Clic en "Validar"
5. Seleccionar método de pago (Efectivo/Cheque/Tarjeta)
6. ¡Terminado!
```

---

## Preguntas frecuentes

### ¿Puedo modificar el abono después de validarlo?
No. Una vez validado, el abono queda registrado definitivamente. Asegúrate de revisar los productos antes de validar.

### ¿Puedo eliminar todos los productos del abono?
Sí. Puedes eliminar los productos uno por uno mientras el abono esté en borrador (antes de validar).

### ¿El stock se actualiza automáticamente?
Sí. Cuando validas el abono, los productos devueltos se suman automáticamente al stock disponible.

### ¿Se puede imprimir el ticket del abono?
Sí. Después de procesar la devolución, puedes imprimir el comprobante del abono como cualquier otro ticket.

### ¿Qué pasa si el cliente pagó con tarjeta pero quiere la devolución en efectivo?
Puedes seleccionar cualquier método de devolución independientemente de cómo pagó originalmente. El sistema solo registra la operación.

---

## Notas importantes

- ✅ Solo puedes crear abonos de tickets que ya estén pagados
- ✅ El abono reduce la deuda del cliente si tiene cuenta corriente
- ✅ Los movimientos de stock quedan registrados en el sistema
- ✅ Todos los abonos quedan vinculados al ticket original
- ✅ El historial completo queda registrado para auditorías

---

**Fecha de actualización**: Enero 2026  
**Versión**: 1.0
