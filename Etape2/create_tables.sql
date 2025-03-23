create table if not exists cars (
    make TEXT,
    model TEXT,
    year INTEGER,
    price FLOAT,
    engine_type TEXT,
    primary key (make,model,year)
);

create table if not exists consumers (
    country TEXT,
    make TEXT,
    model TEXT,
    year INTEGER,
    review_score FLOAT,
    sales_volume INTEGER,
    primary key (country,make,model,year)
);


