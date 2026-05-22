#!/usr/bin/env python3
"""One-off generator for metal and tile material landing pages."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITY_OPTS = """                  <option value="national" selected>National average</option>
                  <option value="dallas">Dallas, TX</option>
                  <option value="phoenix">Phoenix, AZ</option>
                  <option value="austin">Austin, TX</option>
                  <option value="tampa">Tampa, FL</option>
                  <option value="charlotte">Charlotte, NC</option>
                  <option value="raleigh">Raleigh, NC</option>
                  <option value="scottsdale">Scottsdale, AZ</option>
                  <option value="houston">Houston, TX</option>
                  <option value="orlando">Orlando, FL</option>
                  <option value="san-diego">San Diego, CA</option>"""

# Import build logic inline - run metal and tile only with fixed costs
exec(compile(open(__file__).read().replace("if __name__", "if False and __name__"), __file__, "exec"))
