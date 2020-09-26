import pytest
from bs4 import BeautifulSoup
from beautiful_soup_controller import BeautifulSoupController


def test_location_strings():
    answer = """Drop by: Sage Freke,Treasure in:  Tower of Latria"""
    list_string = """
      <ul>
         <li>Drop by: <a class="wiki_link" href="/Sage+Freke,+the+Visionary">Sage Freke</a></li>
         <li>Treasure in: <a class="wiki_link" href="/Tower+of+Latria" title="Tower of Latria"> Tower of Latria</a></li>
      </ul>
      """
    soup = BeautifulSoup(list_string, 'html.parser')
    controller = BeautifulSoupController()
    list_to_check = controller.get_list_of_strings(soup)
    assert answer == list_to_check


def test_get_text_from_column_with_p_tag_and_br():
    answer = "8", "D"
    test_string = """<td> <p>8<br><br>D</p> </td>"""
    soup = BeautifulSoup(test_string, 'html.parser')
    controller = BeautifulSoupController()
    tuple_to_check = controller.get_double_values_from_column(soup)
    assert answer == tuple_to_check


def test_get_text_from_column_with_only_br():
    answer = "9", "D"
    test_string = "<td>9<br/><br/>D </td>"
    soup = BeautifulSoup(test_string, 'html.parser')
    controller = BeautifulSoupController()
    tuple_to_check = controller.get_double_values_from_column(soup.find("td"))
    assert answer == tuple_to_check


def test_get_test_from_column_with_only_p_tag():
    answer = "18", "D"
    test_string = "<td> <p>18</p> <p>D</p> </td>"
    soup = BeautifulSoup(test_string, 'html.parser')
    controller = BeautifulSoupController()
    tuple_to_check = controller.get_double_values_from_column(soup)
    assert answer == tuple_to_check
