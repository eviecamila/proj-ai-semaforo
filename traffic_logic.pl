% Hechos

estado(verde).
estado(amarillo).
estado(rojo).

transicion(verde, amarillo).
transicion(amarillo, rojo).
transicion(rojo, verde).

semaforo(sem1, cruce1, verde, sem2).
semaforo(sem2, cruce1, rojo, sem3).
semaforo(sem3, cruce1, rojo, sem4).
semaforo(sem4, cruce1, rojo, sem1).

semaforo(sem5, cruce2, verde, sem6).
semaforo(sem6, cruce2, rojo, sem7).
semaforo(sem7, cruce2, rojo, sem8).
semaforo(sem8, cruce2, rojo, sem5).

semaforo(sem9, cruce3, verde, sem10).
semaforo(sem10, cruce3, rojo, sem11).
semaforo(sem11, cruce3, rojo, sem12).
semaforo(sem12, cruce3, rojo, sem9).

cruce(cruce1, [blvd_gaxiola, av_bienestar]).
cruce(cruce2, [blvd_gaxiola, blvd_rosendo_g_castro]).
cruce(cruce3, [blvd_gaxiola, lic_benito_juarez]).

:- dynamic semaforo_estado/2. 

semaforo_estado(sem1, verde).
semaforo_estado(sem2, rojo).
semaforo_estado(sem3, rojo).
semaforo_estado(sem4, rojo).
semaforo_estado(sem5, verde).
semaforo_estado(sem6, rojo).
semaforo_estado(sem7, rojo).
semaforo_estado(sem8, rojo).
semaforo_estado(sem9, verde).
semaforo_estado(sem10, rojo).
semaforo_estado(sem11, rojo).
semaforo_estado(sem12, rojo).

colindancia(cruce1, [sem1, sem2, sem3, sem4]).
colindancia(cruce2, [sem5, sem6, sem7, sem8]).
colindancia(cruce3, [sem9, sem10, sem11, sem12]).

% Reglas

estado_cruce(Cruce, Estados) :-
    colindancia(Cruce, Semaforos),
    findall(Estado, (member(Semaforo, Semaforos), semaforo_estado(Semaforo, Estado)), Estados).

sincronizar_cruce(Cruce) :-
    colindancia(Cruce, Semaforos),
    member(SemaforoActual, Semaforos),
    semaforo(SemaforoActual, Cruce, verde, SiguienteSemaforo),
    sincronizar_semaforos(SemaforoActual, SiguienteSemaforo).

sincronizar_semaforos(SemaforoActual, SiguienteSemaforo) :-
    semaforo_estado(SemaforoActual, EstadoActual),
    (EstadoActual == verde -> 
        transicion(EstadoActual, NuevoEstadoActual),
        retract(semaforo_estado(SemaforoActual, EstadoActual)),
        assertz(semaforo_estado(SemaforoActual, NuevoEstadoActual))
    ;
        true
    ),
    semaforo_estado(SemaforoActual, EstadoActual2),
    (EstadoActual2 == amarillo ->
        transicion(EstadoActual2, EstadoFinal),
        retract(semaforo_estado(SemaforoActual, EstadoActual2)),
        assertz(semaforo_estado(SemaforoActual, EstadoFinal))
    ;
        true
    ),
    semaforo_estado(SiguienteSemaforo, EstadoSiguiente),
    (EstadoSiguiente == rojo ->
        transicion(EstadoSiguiente, NuevoEstadoSiguiente),
        retract(semaforo_estado(SiguienteSemaforo, EstadoSiguiente)),
        assertz(semaforo_estado(SiguienteSemaforo, NuevoEstadoSiguiente))
    ;
        true
    ).
