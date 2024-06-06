create table computer_info(
    ip text not null,
    computer_name text not null,
    cpu_temp float,
    cpu_usage float not null,
    memory_usage float not null,
    os text not null,
    created_at timestamp not null
);

select * from computer_info;