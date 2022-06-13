from pathlib import Path

import attr
import pylexibank
from clldutils.misc import slug


@attr.s
class CustomConcept(pylexibank.Concept):
    Number = attr.ib(default=None)
    NumberValue = attr.ib(default=None)


@attr.s
class CustomLanguage(pylexibank.Language):
    Family = attr.ib(default=None)
    Comment = attr.ib(default=None)



@attr.s
class CustomLexeme(pylexibank.Lexeme):
    NumeralAnalysis = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "sand"
    concept_class = CustomConcept
    language_class = CustomLanguage
    lexeme_class = CustomLexeme
    form_spec = pylexibank.FormSpec(replacements=[(" ", "_")])

    def cmd_makecldf(self, args):
        
        args.writer.add_sources()
        concepts = {}
        for concept in self.concepts:
            idx = concept["NUMBER"]+"_"+slug(concept["ENGLISH"])
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["ENGLISH"],
                    Number=concept["NUMBER"],
                    #NumberValue=concept["NUMBER_VALUE"],
                    #Concepticon_ID=concept["CONCEPTICON_ID"],
                    #Concepticon_Gloss=concept["CONCEPTICON_GLOSS"],
                    )
            concepts[concept["ENGLISH"]] = idx
        languages = args.writer.add_languages(lookup_factory="Name")
        for row in self.raw_dir.read_csv("data.tsv", dicts=True,
                delimiter="\t"):
            if row["Concept"] and row["Value"]:
                args.writer.add_forms_from_value(
                        Language_ID=languages[row["Language"]],
                        Parameter_ID=concepts[row["Concept"]],
                        Value=row["Value"],
                        Source="",
                        NumeralAnalysis=row["Analysis"],
                        Comment=row["Comment"]
                        )
        # line only needed for plotting
        for language in languages:
            args.writer.add_forms_from_value(
                    Language_ID=languages[language],
                    Parameter_ID="52_five",
                    Value="dummy"
                    )


