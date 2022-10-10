start(cancun).
city(cancun,"https://goo.gl/maps/P95zJd5ZkPLbZKhJ6").
city(tulum,"https://goo.gl/maps/y8bsP2dQPDxqad8m9").
city(bacalar,"https://goo.gl/maps/AFkZxN7N7CQKTzmw6").
city(merida,"https://goo.gl/maps/R9xdcwD6p9Nq7vyr6").
city(chetumal,"https://goo.gl/maps/DeWhAYJv2AcnpuWU9").


connection(cancun,merida,plain).
connection(cancun,merida,bus).
connection(cancun,tulum,bus).
connection(cancun,bacalar,bus).
connection(cancun,chetumal,plain).
connection(tulum,bacalar,bus).
connection(tulum,chetumal,bus).
connection(chetumal,merida,plain).
connection(chetumal,merida,bus).
connection(chetumal,bacalar,bus).

time(cancun,merida,plain,1).
time(cancun,merida,bus,3).
time(cancun,tulum,bus,2).
time(cancun,bacalar,bus,6).
time(cancun,chetumal,plain,10).
time(tulum,bacalar,bus,3).
time(tulum,chetumal,bus,6).
time(chetumal,merida,plain,1).
time(chetumal,merida,bus,12).
time(chetumal,bacalar,bus,1).