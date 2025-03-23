CREATE TABLE IF NOT EXISTS cars (
    make TEXT,
    model TEXT,
    year INTEGER,
    price FLOAT,
    engine_type TEXT,
    primary key (make,model,year)
);

CREATE TABLE IF NOT EXISTS consumers (
    country TEXT,
    make TEXT,
    model TEXT,
    year INTEGER,
    review_score FLOAT,
    sales_volume INTEGER,
    primary key (country,make,model,year)
);


