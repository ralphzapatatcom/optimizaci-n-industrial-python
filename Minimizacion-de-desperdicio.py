import pulp # Una librería excelente para ingenieros industriales

# 1. Definir el problema
prob = pulp.LpProblem("Optimizacion_Corte_Tela", pulp.LpMinimize)

# 2. Definir posibles combinaciones de corte en un rollo de 10m
# Formato: (Camisas, Pantalones, Desperdicio)
patrones = [
    (8, 0, 0.4), # 8*1.2 + 0*1.8 = 9.6m (Sobran 0.4)
    (0, 5, 1.0), # 0*1.2 + 5*1.8 = 9.0m (Sobra 1.0)
    (4, 2, 1.6), # 4*1.2 + 2*1.8 = 8.4m (Sobra 1.6)
    (2, 4, 0.4), # 2*1.2 + 4*1.8 = 9.6m (Sobran 0.4)
    (5, 2, 0.4)  # 5*1.2 + 2*1.8 = 9.6m (Sobran 0.4)
]

# 3. Variables de decisión: Cuántos rollos usar de cada patrón
x = [pulp.LpVariable(f"Rollo_Patron_{i}", lowBound=0, cat='Integer') for i in range(len(patrones))]

# 4. Función Objetivo: Minimizar el desperdicio total
prob += pulp.lpSum([x[i] * patrones[i][2] for i in range(len(patrones))])

# 5. Restricciones de demanda
# Camisas totales >= 100
prob += pulp.lpSum([x[i] * patrones[i][0] for i in range(len(patrones))]) >= 100
# Pantalones totales >= 50
prob += pulp.lpSum([x[i] * patrones[i][1] for i in range(len(patrones))]) >= 50

# 6. Resolver
prob.solve()

# Resultados
print(f"Estado: {pulp.LpStatus[prob.status]}")
for i in range(len(patrones)):
    if x[i].varValue > 0:
        print(f"Usar {x[i].varValue} rollos con el patrón {i+1} {patrones[i][:2]}")

print(f"Desperdicio total: {pulp.value(prob.objective):.2f} metros")