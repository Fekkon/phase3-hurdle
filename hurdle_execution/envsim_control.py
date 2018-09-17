#!/usr/bin/env python3

import argparse
import configparser
import subprocess
import sys


def main():
    # set up command line args
    parser = argparse.ArgumentParser(prog="envsim_control",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--mode", default="hurdle", choices=["hurdle", "bot-debug"],
                        help="for internal use only. Not supported for external users")

    parser.add_argument('--enable-debug-output', action="store_true", default=False,
                        help=("When specified, this flag will run the envsim with a ZMQ push socket that" +
                              " outputs the samples sent to competitor containers"))

    subparsers = parser.add_subparsers(dest='action')

    # subparser for "stop" action. No args required, but doing it this way to make the commands
    # feel less wonky on the CLI
    _ = subparsers.add_parser('stop',
                              formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # subparser for "start" action.
    parser_start = subparsers.add_parser('start',
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser_start.add_argument("--samp-rate", type=float, default=100e3,
                              help="sample rate of the environment simulator")

    parser_start.add_argument("--host", default="192.168.40.2",
                              help="Host name that the simulator listens on for incoming samples")

    parser_start.add_argument("--port-num-base", type=int, default=52000,
                              help="Port number to start incrementing from for envsim ports")

    parser_start.add_argument("--noise-amp", type=float, default=0.001,
                              help="amplitude of the environment simulator background noise")

    parser_start.add_argument("--envsim-config-file", default="/root/phase3-hurdle/gr-envsim/apps/envsim.ini",
                              help="This should be set to where the envsim service expect to find its config file")

    parser_start.add_argument("--usrp-ip-prefix", default="192.168.40.",
                              help="First 3 octets of IPs to send samples to")

    parser_start.add_argument("--usrp-ip-base", default=101, type=int,
                              help="starting point for last octet of IPs to send samples to")

    parser_start.add_argument("--channel-gain-linear", type=float, default=0.01,
                              help="scalar applied to channels, linear (not log) scaled")

    # parse args and store to dictionary
    args = vars(parser.parse_args())

    # stop the envsim server if commanded to do so
    if args["action"] == "stop":

        if args["mode"] == "hurdle":
            if args["enable_debug_output"]:
                stop_cmd = ["systemctl", "stop", "envsim-debug-output"]
            else:
                stop_cmd = ["systemctl", "stop", "envsim"]

        elif args["mode"] == "bot-debug":
            stop_cmd = ["systemctl", "stop", "envsim-bot-debug"]
        else:
            raise ValueError("Unknown mode {} specified".format(args["mode"]))

        print("Stopping envsim")
        print("running {}".format(" ".join(stop_cmd)))
        subprocess.run(stop_cmd)

        sys.exit(0)
    # otherwise we must be starting
    else:

        # first build up ini file contents
        config = configparser.ConfigParser()
        config['main'] = {"samp_rate": args["samp_rate"],
                          "host_ip": args["host"],
                          "port_num_base": args["port_num_base"],
                          "noise_amp": args["noise_amp"],
                          "channel_gain_linear": args["channel_gain_linear"],
                          "usrp_ip_base": args["usrp_ip_base"],
                          "usrp_ip_prefix": args["usrp_ip_prefix"],
                          "increment_usrp_address": True
                          }

        # now write out contents
        with open(args["envsim_config_file"], 'w') as configfile:
            config.write(configfile)

        # now start the service
        if args["mode"] == "hurdle":
            if args["enable_debug_output"]:
                start_cmd = ["systemctl", "start", "envsim-debug-output"]
            else:
                start_cmd = ["systemctl", "start", "envsim"]
        elif args["mode"] == "bot-debug":
            start_cmd = ["systemctl", "start", "envsim-bot-debug"]
        else:
            raise ValueError("Unknown mode {} specified".format(args["mode"]))

        print("Starting envsim")
        print("running {}".format(" ".join(start_cmd)))
        subprocess.run(start_cmd)

        sys.exit(0)


if __name__ == "__main__":
    main()
