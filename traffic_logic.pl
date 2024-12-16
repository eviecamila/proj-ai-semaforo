% Estados de los semáforos
estado(verde).
estado(amarillo).
estado(rojo).

% Semáforos con su estado inicial
:- dynamic semaforo_estado/2.
semaforo_estado(sem1, verde).
semaforo_estado(sem2, rojo).
semaforo_estado(sem3, rojo).
semaforo_estado(sem4, rojo).

% Secuencia de estados personalizados
secuencia([
    [verde, rojo, rojo, rojo],    % G R R R
    [amarillo, rojo, rojo, rojo], % Y R R R
    [rojo, verde, rojo, rojo],    % R G R R
    [rojo, amarillo, rojo, rojo], % R Y R R
    [rojo, rojo, verde, rojo],    % R R G R
    [rojo, rojo, amarillo, rojo], % R R Y R
    [rojo, rojo, rojo, verde],    % R R R G
    [rojo, rojo, rojo, amarillo], % R R R Y
    [rojo, rojo, rojo, rojo]      % R R R R
]).

% Índice dinámico para la secuencia
:- dynamic indice_secuencia/1.
indice_secuencia(1).  % Comenzamos en la primera posición de la secuencia

% Avanzar al siguiente estado en la secuencia
avanzar_estado :-
    secuencia(Secuencia),
    indice_secuencia(IndiceActual),
    length(Secuencia, Longitud),
    nth1(IndiceActual, Secuencia, EstadosActuales),  % Obtener el estado actual
    actualizar_estados(EstadosActuales),            % Actualizar semáforos
    siguiente_indice(IndiceActual, Longitud).       % Calcular el siguiente índice

% Calcular el siguiente índice cíclico
siguiente_indice(IndiceActual, Longitud) :-
    NuevoIndice is (IndiceActual mod Longitud) + 1,
    retractall(indice_secuencia(_)),  % Eliminar el índice anterior
    assertz(indice_secuencia(NuevoIndice)).

% Actualizar los estados dinámicos de los semáforos
actualizar_estados([E1, E2, E3, E4]) :-
    retractall(semaforo_estado(sem1, _)),
    assertz(semaforo_estado(sem1, E1)),
    retractall(semaforo_estado(sem2, _)),
    assertz(semaforo_estado(sem2, E2)),
    retractall(semaforo_estado(sem3, _)),
    assertz(semaforo_estado(sem3, E3)),
    retractall(semaforo_estado(sem4, _)),
    assertz(semaforo_estado(sem4, E4)),
    format('Estados actualizados: ~w, ~w, ~w, ~w~n', [E1, E2, E3, E4]).



% Consultar el estado actual de los semáforos
estado_actual([Sem1, Sem2, Sem3, Sem4], [E1, E2, E3, E4]) :-
    semaforo_estado(Sem1, E1),
    semaforo_estado(Sem2, E2),
    semaforo_estado(Sem3, E3),
    semaforo_estado(Sem4, E4).
