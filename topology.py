
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.topo import Topo


class ExamTopo(Topo):

    def build(self):

        # Examination server
        server = self.addHost(
            "h1",
            ip="10.0.0.1/24"
        )

        # Student clients
        student1 = self.addHost(
            "h2",
            ip="10.0.0.2/24"
        )

        student2 = self.addHost(
            "h3",
            ip="10.0.0.3/24"
        )

        # OpenFlow switch
        switch = self.addSwitch(
            "s1",
            protocols="OpenFlow13"
        )

        # Connect hosts to switch
        self.addLink(server, switch, cls=TCLink, bw=10, delay="5ms")
        self.addLink(student1, switch, cls=TCLink, bw=5, delay="5ms")
        self.addLink(student2, switch, cls=TCLink, bw=10, delay="5ms")


def start_network():

    topo = ExamTopo()

    net = Mininet(
        topo=topo,
        switch=OVSSwitch,
        controller=None,
        link=TCLink,
        autoSetMacs=True
    )

    # Connect to external SDN controller
    net.addController(
        "c0",
        controller=RemoteController,
        ip="127.0.0.1",
        port=6653
    )

    print("\nStarting Online Examination Network...")

    net.start()

    print("\nNetwork topology is running!")
    print("h1 = Examination Server")
    print("h2 = Student 1")
    print("h3 = Student 2")

    print("\nServer IP: 10.0.0.1")
    print("Server Port: 5000")

    CLI(net)

    net.stop()


if __name__ == "__main__":
    start_network()
