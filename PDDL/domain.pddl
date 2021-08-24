(define (domain dialogplan3)

(:requirements :strips :conditional-effects)

(:predicates 
    (status-unknown-db-access ?x)
    (status-unknown-user-query ?x)
    (status-known-user-query ?x)
    (status-known-db-access ?x)
    (status-have-user-query ?x)
    (status-have-exact-query ?x)
    (status-have-partial-query ?x)
    (is_query_exact ?x)
    (is_query_partial ?x)
    (status-display-result ?x)
    (status-display-code ?x)
)

(:action GET_USER_QUERY
    :parameters (?x)
    :precondition (and (status-unknown-user-query ?x))
    :effect (and (status-known-user-query ?x)
            (status-unknown-db-access ?x))
)


(:action GET_DB_ACCESS
    :parameters (?x)
    :precondition (and (status-unknown-db-access ?x))
    :effect (and (status-known-db-access ?x)
                (status-have-user-query ?x))
)


(:action CHECK_QUERY_TYPE
    :parameters (?x)
    :precondition (and (status-have-user-query ?x))
    :effect (and (when (is_query_exact ?x) (status-have-exact-query ?x))
                (when (is_query_partial ?x) (status-have-partial-query ?x))
    )
)

(:action DISPLAY_EXACT_MATCH_RESULTS
    :parameters (?x)
    :precondition (and (status-have-exact-query ?x))
    :effect (and (status-display-result ?x))
)

(:action PERFORM_PARTIAL_MATCH_DISAMBIGUATION
    :parameters (?x)
    :precondition (and (status-have-partial-query ?x))
    :effect (and (status-have-user-query ?x)
    )
)
)